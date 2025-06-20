import json
import pandas as pd

def extract_avg_monthly_revenue(monthly_revenue_list):
    revenues = []
    for item in monthly_revenue_list:
        for _, value in item.items():
            try:
                revenues.append(float(value))
            except Exception:
                pass
    return sum(revenues) / len(revenues) if revenues else 0.0

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def safe_int(val):
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0

def process_lender_offer_dataset(json_path, csv_path):
    with open(json_path, 'r') as f:
        # If your file is line-delimited JSON, use:
        data = [json.loads(line) for line in f if line.strip()]
        # If your file is a single JSON array, use:
        # data = json.load(f)

    rows = []
    for item in data:
        merchant = item.get('merchant_details', {})
        avg_revenue = extract_avg_monthly_revenue(merchant.get('monthly_revenue', []))
        business_type = merchant.get('business_type', '')
        entity_type = merchant.get('entity_type', '')
        state = merchant.get('state', '')
        credit_score = safe_int(merchant.get('credit_score', 0))
        months_in_business = safe_int(merchant.get('months_in_business', 0))
        requested_amount = safe_float(merchant.get('requested_amount', 0))

        for offer in item.get('lender_offers', []):
            row = {
                'merchant_details.business_type': business_type,
                'merchant_details.entity_type': entity_type,
                'merchant_details.state': state,
                'merchant_details.credit_score': credit_score,
                'merchant_details.months_in_business': months_in_business,
                'merchant_details.requested_amount': requested_amount,
                'avg_monthly_revenue': avg_revenue,
                'lender_name': offer.get('lender_name', ''),
                'payment_amount': safe_float(offer.get('payment_amount', 0)),
                'funding_amount': safe_float(offer.get('funding_amount', 0)),
                'factor_rate': safe_float(offer.get('factor_rate', 0)),
                'rtr': safe_float(offer.get('rtr', 0)),
                'terms': safe_int(offer.get('terms', 0)),
                'term_type': offer.get('term_type', '')
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    print(f"✅ CSV saved to {csv_path}")

# Example usage:
# process_lender_offer_dataset('data/raw/lender_offers.json', 'data/processed/processed_lender_offers.csv')