#!/usr/bin/env python3
"""
Council Tax Fraud Detection CLI Demo
Quick demonstration of the fraud detection capabilities
"""

from fraud_detector import CouncilTaxFraudDetector, FraudType, RiskLevel
from data_generator import generate_sample_cases
import json

def print_separator():
    print("=" * 80)

def demonstrate_detection():
    print("\n🛡️  COUNCIL TAX FRAUD PREVENTION SYSTEM - CLI DEMO")
    print_separator()
    
    # Initialize detector
    detector = CouncilTaxFraudDetector()
    
    # Example 1: Clear fraud case
    print("\n📋 CASE 1: Single Person Discount Fraud")
    print("-" * 40)
    
    fraud_case = {
        'case_id': 'DEMO-001',
        'multiple_utility_accounts': True,
        'electoral_register_mismatch': True,
        'social_media_evidence': True,
        'multiple_vehicles': True,
        'multiple_utility_accounts_evidence': '3 utility accounts: John Smith, Jane Doe, J Smith',
        'electoral_register_mismatch_evidence': 'Electoral roll shows 2 adults registered',
        'social_media_evidence_evidence': 'Facebook shows couple living together',
        'multiple_vehicles_evidence': '2 vehicles registered: BMW X5, Audi A4'
    }
    
    result = detector.detect_fraud(fraud_case)
    
    print(f"Risk Level: {result.risk_level.value.upper()}")
    print(f"Risk Score: {result.risk_score:.2%}")
    print(f"Classification: {'FRAUD' if result.is_likely_fraud else 'ERROR' if result.is_likely_error else 'UNCERTAIN'}")
    print(f"Confidence: {result.confidence:.1%}")
    print("\nDetected Indicators:")
    for ind in result.indicators[:3]:
        if ind.detected:
            print(f"  • {ind.description}")
    print("\nRecommended Actions:")
    for rec in result.recommendations[:3]:
        print(f"  → {rec}")
    
    # Example 2: Cuckooing case
    print("\n📋 CASE 2: Suspected Cuckooing")
    print("-" * 40)
    
    cuckooing_case = {
        'case_id': 'DEMO-002',
        'sudden_payment_regularity': True,
        'vulnerable_resident': True,
        'antisocial_reports': True,
        'behavior_change': True,
        'payment_source_change': True,
        'police_intelligence': True
    }
    
    result = detector.detect_fraud(cuckooing_case)
    
    print(f"Risk Level: {result.risk_level.value.upper()}")
    print(f"Risk Score: {result.risk_score:.2%}")
    print(f"Fraud Type: {result.fraud_type.value if result.fraud_type else 'Unknown'}")
    print("\n⚠️  SAFEGUARDING ALERT - Vulnerable person at risk")
    print("\nUrgent Actions:")
    for rec in result.recommendations[:3]:
        print(f"  → {rec}")
    
    # Example 3: Likely error case
    print("\n📋 CASE 3: Likely Administrative Error")
    print("-" * 40)
    
    error_case = {
        'case_id': 'DEMO-003',
        'electoral_register_mismatch': True,
        'immediate_cooperation': True,
        'consistent_explanation': True,
        'self_reported': True,
        'recent_life_change': True,
        'first_occurrence': True
    }
    
    result = detector.detect_fraud(error_case)
    
    print(f"Risk Level: {result.risk_level.value.upper()}")
    print(f"Risk Score: {result.risk_score:.2%}")
    print(f"Classification: {'ERROR - No fraud suspected' if result.is_likely_error else 'Requires review'}")
    print("\nMitigating Factors:")
    for ind in result.indicators:
        if ind.detected and ind.weight < 0:
            print(f"  ✓ {ind.description}")
    print("\nRecommended Approach:")
    for rec in result.recommendations[:2]:
        print(f"  → {rec}")
    
    # Batch analysis
    print("\n📊 BATCH ANALYSIS: Processing 50 Cases")
    print("-" * 40)
    
    sample_cases = generate_sample_cases(50)
    batch_results = detector.batch_analyze(sample_cases)
    
    stats = batch_results['statistics']
    print(f"Total Cases Analyzed: {stats['total_cases']}")
    print(f"High Risk Cases: {stats['high_risk']} ({stats['high_risk']/stats['total_cases']*100:.1f}%)")
    print(f"Likely Fraud: {stats['likely_fraud']} ({stats['likely_fraud']/stats['total_cases']*100:.1f}%)")
    print(f"Likely Errors: {stats['likely_error']} ({stats['likely_error']/stats['total_cases']*100:.1f}%)")
    
    if stats['by_type']:
        print("\nFraud Types Detected:")
        for fraud_type, count in stats['by_type'].items():
            print(f"  • {fraud_type.replace('_', ' ').title()}: {count} cases")
    
    print_separator()
    print("\n✅ Demo Complete - System Ready for Deployment")
    print("\nKey Features Demonstrated:")
    print("  • Multi-pattern fraud detection")
    print("  • Fraud vs Error classification")
    print("  • Cuckooing/vulnerability detection")
    print("  • Risk scoring and prioritization")
    print("  • Actionable recommendations")
    print("\nTo launch the web dashboard, run:")
    print("  streamlit run src/dashboard.py")

if __name__ == "__main__":
    demonstrate_detection()