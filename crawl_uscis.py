import requests
from bs4 import BeautifulSoup, Tag
import json
from concurrent.futures import ThreadPoolExecutor
import argparse


def url_from_rid(receipt_id):
    return (
        f"https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum={receipt_id}"
    )


def get_status(rid):
    url = url_from_rid(rid)

    result = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    for div in soup.find("div", attrs={"class": ["appointment-sec", "text-center"]}):
        p = div.find("p")
        if isinstance(p, Tag):
            result["Description"] = p.text.split("<p>")[-1].split("</p")[0]
        h = div.find("h1")
        if isinstance(h, Tag):
            result["Title"] = h.text.split("<h1>")[-1].split("</h1")[0]

    for div in soup.find("div", {"id": "formErrorMessages"}):
        l = div.find("li")
        if isinstance(l, Tag):
            result["error"] = l.text.split("<li>")[-1].split("</li")[0]

    return result


def accum_stats(title, stats, before=True):
    if before:
        key = "Before"
    else:
        key = "After"
    if "Approved" in title:
        stats[key]["Approved"] += 1
    elif "Request for Additional Evidence" in title:
        stats[key]["RFE"] += 1
    elif "Received" in title:
        stats[key]["Received"] += 1
    elif "Updated To Show Fingerprints" in title:
        stats[key]["Fingerprints taken"] += 1
    elif "Rejected" in title:
        stats[key]["Rejected"] += 1
    else:
        stats[key]["Other"] += 1

    return stats


def crawl_uscis(receipt_prefix, receipt_nums, crawl_range):

    print("Your Summary:\n")
    for receipt_num in receipt_nums:
        results = get_status(receipt_prefix + str(receipt_num))
        for k, v in results.items():
            print(f"{k}: {v}")
        print("\n")

    stats = {
        "Before": {
            "Approved": 0,
            "RFE": 0,
            "Received": 0,
            "Other": 0,
            "Rejected": 0,
            "Fingerprints taken": 0,
        },
        "After": {
            "Approved": 0,
            "RFE": 0,
            "Received": 0,
            "Other": 0,
            "Rejected": 0,
            "Fingerprints taken": 0,
        },
    }
    results = {}

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        last_receipt_num = int(receipt_nums[-1])
        for i in range(last_receipt_num - crawl_range, last_receipt_num + crawl_range):
            result = futures.append(
                (i, executor.submit(get_status, receipt_prefix + str(i)))
            )

        for future in futures:
            receipt_idx, result_future = future
            result = result_future.result()
            results[receipt_idx] = result
            if not any(
                [
                    check in result["Description"]
                    for check in ["I-131", "I-485", "I-765"]
                ]
            ):
                continue
            if "Title" in result:  # Just checking to make sure it's not an error
                stats = accum_stats(
                    result["Title"], stats, receipt_idx > last_receipt_num
                )

    print("Analyzing neighbors:\n")
    for k, v in stats.items():
        print(f"\nStats from {k} your receipt number")
        all_apps = sum(v.values())
        for v1, v2 in v.items():
            print(f"{v1}:{v2}/{all_apps}")

    return results


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Command line interface to compute comparative metrics on sets of queries in database."
    )
    parser.add_argument(
        "--receipt_prefix", help="USCIS given receipt prefix.", type=str, default="MSC"
    )
    parser.add_argument(
        "--receipt_nums",
        help="USCIS given receipt number.",
        type=list,
        default=["2290262024", "2290262025", "2290262026"],
    )
    parser.add_argument(
        "--crawl_range", help="+- receipt numbers to crawl", type=int, default=100
    )

    args = parser.parse_args()

    results = crawl_uscis(args.receipt_prefix, args.receipt_nums, args.crawl_range)

    with open("uscis_crawls.json", "w") as f:
        json.dump(results, f)
    print("\nYour Neighbors summary stored to uscis_crawls.json")
