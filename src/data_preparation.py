import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split

def process_lender_offer_dataset(input_path: str, output_path: str) -> None:
    # Open the JSON file and load its content
    with open(input_path, 'r') as f:
        json_data = json.load(f)

    processed_rows = []
    for record in json_data:
        merchant = record.get("merchant_details", {})
        offers = record.get("lender_offers", [])

        # Calculate average monthly revenue
        rev_values = []
        for r in merchant.get("monthly_revenue", []):
            for val in r.values():
                try:
                    rev_values.append(float(val))
                except:
                    pass
        avg_rev = sum(rev_values) / len(rev_values) if rev_values else 0

        for offer in offers:
            processed_rows.append({
                "merchant_details.business_type": merchant.get("business_type", ""),
                "merchant_details.entity_type": merchant.get("entity_type", ""),
                "merchant_details.state": merchant.get("state", ""),
                "merchant_details.credit_score": int(merchant.get("credit_score") or 0),
                "merchant_details.months_in_business": int(merchant.get("months_in_business") or 0),
                "merchant_details.requested_amount": float(merchant.get("requested_amount") or 0),
                "merchant_details.avg_monthly_revenue": avg_rev,
                "lender_offer.lender_name": offer.get("lender_name", ""),
                "lender_offer.funding_amount": float(offer.get("payment_amount") or 0),
                "lender_offer.payment_amount": float(offer.get("funding_amount") or 0),
                "lender_offer.factor_rate": float(offer.get("factor_rate") or 0),
                "lender_offer.rtr": float(offer.get("rtr") or 0),
                "lender_offer.terms": int(offer.get("terms") or 0),
                "lender_offer.term_type": offer.get("term_type", ""),
            })

    # Save processed data to a CSV file
    df = pd.DataFrame(processed_rows)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Processed data saved to {output_path}")

