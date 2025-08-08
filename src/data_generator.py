import random
from typing import List, Dict
from datetime import datetime, timedelta

def generate_sample_cases(num_cases: int = 100) -> List[Dict]:
    """Generate sample council tax cases for testing"""
    
    cases = []
    
    # Fraud patterns for realistic data
    fraud_patterns = {
        'single_person_discount': {
            'indicators': ['multiple_utility_accounts', 'electoral_register_mismatch', 
                          'social_media_evidence', 'multiple_vehicles', 'credit_check_mismatch'],
            'probability': 0.25
        },
        'student_exemption': {
            'indicators': ['post_graduation_claim', 'employment_income', 'part_time_status',
                          'fake_documentation', 'historical_pattern'],
            'probability': 0.20
        },
        'empty_property': {
            'indicators': ['utility_usage', 'rental_listings', 'neighbor_reports',
                          'maintenance_activity', 'postal_deliveries'],
            'probability': 0.15
        },
        'cuckooing': {
            'indicators': ['sudden_payment_regularity', 'behavior_change', 'antisocial_reports',
                          'vulnerable_resident', 'payment_source_change', 'police_intelligence'],
            'probability': 0.10
        }
    }
    
    error_indicators = ['immediate_cooperation', 'consistent_explanation', 
                       'documentation_provided', 'self_reported', 'first_occurrence',
                       'recent_life_change']
    
    for i in range(num_cases):
        case = {
            'case_id': f'CASE-2024-{i+1:04d}',
            'property_id': f'PROP-{random.randint(1000, 9999)}',
            'account_holder': f'Person_{i+1}',
            'address': f'{random.randint(1, 999)} {random.choice(["High", "Main", "Church", "Park", "Victoria"])} Street',
            'council_tax_band': random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']),
            'annual_charge': random.randint(800, 3500),
            'current_discount': random.choice(['None', 'Single Person', 'Student', 'Empty', 'Disability']),
            'payment_history': random.choice(['Regular', 'Irregular', 'Delinquent', 'Recently Improved']),
            'account_age_years': random.randint(1, 20),
            'last_review_date': (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d')
        }
        
        # Determine if this is a fraud, error, or legitimate case
        case_type = random.choices(['fraud', 'error', 'legitimate'], 
                                  weights=[0.3, 0.2, 0.5])[0]
        
        if case_type == 'fraud':
            # Select fraud type
            fraud_type = random.choice(list(fraud_patterns.keys()))
            pattern = fraud_patterns[fraud_type]
            
            # Add fraud indicators (70-90% of them)
            num_indicators = random.randint(
                int(len(pattern['indicators']) * 0.7),
                len(pattern['indicators'])
            )
            selected_indicators = random.sample(pattern['indicators'], num_indicators)
            
            for indicator in selected_indicators:
                case[indicator] = True
                case[f'{indicator}_evidence'] = f'Evidence for {indicator.replace("_", " ")}'
            
            # Low chance of error indicators in fraud cases
            if random.random() < 0.1:
                error_ind = random.choice(error_indicators)
                case[error_ind] = True
                
        elif case_type == 'error':
            # Add some fraud indicators (20-40%)
            all_fraud_indicators = []
            for pattern in fraud_patterns.values():
                all_fraud_indicators.extend(pattern['indicators'])
            
            num_fraud_indicators = random.randint(1, 3)
            selected_fraud = random.sample(all_fraud_indicators, 
                                         min(num_fraud_indicators, len(all_fraud_indicators)))
            
            for indicator in selected_fraud:
                case[indicator] = True
                case[f'{indicator}_evidence'] = f'Possible {indicator.replace("_", " ")}'
            
            # Add error indicators (60-80%)
            num_error_indicators = random.randint(
                int(len(error_indicators) * 0.6),
                int(len(error_indicators) * 0.8)
            )
            selected_errors = random.sample(error_indicators, num_error_indicators)
            
            for indicator in selected_errors:
                case[indicator] = True
        
        else:  # legitimate
            # Very few or no indicators
            if random.random() < 0.2:
                # Add 1-2 benign indicators
                all_indicators = error_indicators.copy()
                num_indicators = random.randint(1, 2)
                selected = random.sample(all_indicators, num_indicators)
                for indicator in selected:
                    case[indicator] = True
        
        # Add metadata
        case['data_quality_score'] = random.uniform(0.6, 1.0)
        case['last_contact_days_ago'] = random.randint(0, 365)
        case['num_previous_investigations'] = random.choices([0, 1, 2, 3], 
                                                            weights=[0.7, 0.2, 0.08, 0.02])[0]
        
        # Special handling for cuckooing cases
        if 'vulnerable_resident' in case and case.get('vulnerable_resident'):
            case['resident_age'] = random.choice([random.randint(70, 95), random.randint(18, 25)])
            case['disability_registered'] = random.choice([True, False])
            case['social_services_involved'] = random.choice([True, False])
        
        cases.append(case)
    
    return cases

def generate_historical_data(days: int = 30) -> Dict:
    """Generate historical trend data"""
    
    data = {
        'dates': [],
        'total_cases': [],
        'fraud_detected': [],
        'errors_detected': [],
        'investigations_opened': [],
        'prosecutions': [],
        'amount_recovered': []
    }
    
    base_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        data['dates'].append(current_date.strftime('%Y-%m-%d'))
        
        # Simulate daily metrics with some patterns
        day_of_week = current_date.weekday()
        
        # More activity on weekdays
        weekday_multiplier = 1.5 if day_of_week < 5 else 0.7
        
        data['total_cases'].append(int(random.randint(80, 120) * weekday_multiplier))
        data['fraud_detected'].append(int(random.randint(5, 15) * weekday_multiplier))
        data['errors_detected'].append(int(random.randint(10, 25) * weekday_multiplier))
        data['investigations_opened'].append(random.randint(2, 8))
        data['prosecutions'].append(random.choices([0, 1, 2], weights=[0.7, 0.25, 0.05])[0])
        data['amount_recovered'].append(random.randint(5000, 50000))
    
    return data

def generate_performance_metrics() -> Dict:
    """Generate system performance metrics"""
    
    return {
        'detection_accuracy': random.uniform(0.85, 0.95),
        'false_positive_rate': random.uniform(0.05, 0.15),
        'average_processing_time_ms': random.randint(50, 200),
        'cases_processed_today': random.randint(200, 500),
        'alerts_generated': random.randint(20, 50),
        'high_risk_cases': random.randint(5, 15),
        'system_uptime_percent': random.uniform(99.0, 99.99),
        'last_model_update': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
        'active_investigations': random.randint(30, 80),
        'pending_reviews': random.randint(50, 150)
    }

if __name__ == "__main__":
    # Test data generation
    sample_cases = generate_sample_cases(5)
    for case in sample_cases:
        print(f"Case {case['case_id']}: {case.get('current_discount', 'None')} discount")
        indicators = [k for k, v in case.items() if v is True and not k.endswith('_evidence')]
        if indicators:
            print(f"  Indicators: {', '.join(indicators[:3])}")
    
    print("\nHistorical data sample:")
    hist_data = generate_historical_data(7)
    for i in range(min(3, len(hist_data['dates']))):
        print(f"  {hist_data['dates'][i]}: {hist_data['fraud_detected'][i]} frauds, {hist_data['errors_detected'][i]} errors")
    
    print("\nPerformance metrics:")
    metrics = generate_performance_metrics()
    print(f"  Detection accuracy: {metrics['detection_accuracy']:.2%}")
    print(f"  Cases processed today: {metrics['cases_processed_today']}")