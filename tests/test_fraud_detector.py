import unittest
import sys
sys.path.append('../src')
from fraud_detector import CouncilTaxFraudDetector, FraudType, RiskLevel

class TestFraudDetector(unittest.TestCase):
    
    def setUp(self):
        self.detector = CouncilTaxFraudDetector()
    
    def test_single_person_discount_fraud(self):
        """Test detection of single person discount fraud"""
        case = {
            'case_id': 'TEST-001',
            'multiple_utility_accounts': True,
            'electoral_register_mismatch': True,
            'social_media_evidence': True,
            'multiple_vehicles': True
        }
        
        result = self.detector.detect_fraud(case)
        
        self.assertEqual(result.fraud_type, FraudType.SINGLE_PERSON_DISCOUNT)
        self.assertTrue(result.is_likely_fraud)
        self.assertFalse(result.is_likely_error)
        self.assertIn(result.risk_level, [RiskLevel.HIGH, RiskLevel.CRITICAL])
    
    def test_cuckooing_detection(self):
        """Test detection of cuckooing (vulnerable person exploitation)"""
        case = {
            'case_id': 'TEST-002',
            'sudden_payment_regularity': True,
            'vulnerable_resident': True,
            'antisocial_reports': True,
            'behavior_change': True,
            'police_intelligence': True
        }
        
        result = self.detector.detect_fraud(case)
        
        self.assertEqual(result.fraud_type, FraudType.CUCKOOING)
        self.assertTrue(result.is_likely_fraud)
        # Check for safeguarding recommendations
        recommendations_text = ' '.join(result.recommendations)
        self.assertIn('safeguarding', recommendations_text.lower())
    
    def test_error_detection(self):
        """Test detection of administrative errors vs fraud"""
        case = {
            'case_id': 'TEST-003',
            'electoral_register_mismatch': True,
            'immediate_cooperation': True,
            'consistent_explanation': True,
            'self_reported': True,
            'first_occurrence': True
        }
        
        result = self.detector.detect_fraud(case)
        
        self.assertTrue(result.is_likely_error)
        self.assertFalse(result.is_likely_fraud)
        self.assertEqual(result.risk_level, RiskLevel.LOW)
        # Check for educational recommendations
        recommendations_text = ' '.join(result.recommendations)
        self.assertIn('educational', recommendations_text.lower())
    
    def test_empty_property_fraud(self):
        """Test detection of empty property fraud"""
        case = {
            'case_id': 'TEST-004',
            'utility_usage': True,
            'rental_listings': True,
            'neighbor_reports': True
        }
        
        result = self.detector.detect_fraud(case)
        
        self.assertEqual(result.fraud_type, FraudType.EMPTY_PROPERTY)
        self.assertTrue(result.is_likely_fraud)
    
    def test_risk_scoring(self):
        """Test risk scoring algorithm"""
        # Low risk case
        low_risk_case = {
            'case_id': 'TEST-005',
            'self_reported': True
        }
        low_result = self.detector.detect_fraud(low_risk_case)
        self.assertEqual(low_result.risk_level, RiskLevel.LOW)
        self.assertLess(low_result.risk_score, 0.25)
        
        # High risk case
        high_risk_case = {
            'case_id': 'TEST-006',
            'multiple_utility_accounts': True,
            'electoral_register_mismatch': True,
            'social_media_evidence': True,
            'credit_check_mismatch': True
        }
        high_result = self.detector.detect_fraud(high_risk_case)
        self.assertIn(high_result.risk_level, [RiskLevel.HIGH, RiskLevel.CRITICAL])
        self.assertGreater(high_result.risk_score, 0.5)
    
    def test_batch_analysis(self):
        """Test batch processing of multiple cases"""
        cases = [
            {'case_id': 'BATCH-001', 'multiple_utility_accounts': True},
            {'case_id': 'BATCH-002', 'self_reported': True},
            {'case_id': 'BATCH-003', 'utility_usage': True, 'rental_listings': True}
        ]
        
        results = self.detector.batch_analyze(cases)
        
        self.assertEqual(results['statistics']['total_cases'], 3)
        self.assertIn('assessments', results)
        self.assertEqual(len(results['assessments']), 3)
        self.assertIn('by_type', results['statistics'])
    
    def test_confidence_scoring(self):
        """Test confidence calculation"""
        # High confidence case (many indicators)
        high_conf_case = {
            'case_id': 'TEST-007',
            'multiple_utility_accounts': True,
            'electoral_register_mismatch': True,
            'social_media_evidence': True,
            'multiple_vehicles': True,
            'credit_check_mismatch': True
        }
        high_conf_result = self.detector.detect_fraud(high_conf_case)
        self.assertGreater(high_conf_result.confidence, 0.6)
        
        # Low confidence case (few indicators)
        low_conf_case = {
            'case_id': 'TEST-008',
            'multiple_vehicles': True
        }
        low_conf_result = self.detector.detect_fraud(low_conf_case)
        self.assertLess(low_conf_result.confidence, 0.5)
    
    def test_recommendations_generation(self):
        """Test that appropriate recommendations are generated"""
        # Critical risk should have immediate action recommendations
        critical_case = {
            'case_id': 'TEST-009',
            'post_graduation_claim': True,
            'employment_income': True,
            'fake_documentation': True,
            'historical_pattern': True
        }
        critical_result = self.detector.detect_fraud(critical_case)
        
        self.assertGreater(len(critical_result.recommendations), 0)
        recommendations_text = ' '.join(critical_result.recommendations)
        self.assertIn('investigation', recommendations_text.lower())
        
        # Low risk should have monitoring recommendations
        low_risk_case = {
            'case_id': 'TEST-010',
            'first_occurrence': True,
            'immediate_cooperation': True
        }
        low_result = self.detector.detect_fraud(low_risk_case)
        
        self.assertGreater(len(low_result.recommendations), 0)
        low_recommendations = ' '.join(low_result.recommendations)
        self.assertTrue(
            'watchlist' in low_recommendations.lower() or 
            'educational' in low_recommendations.lower()
        )

if __name__ == '__main__':
    unittest.main()