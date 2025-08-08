from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime, timedelta
import random

class FraudType(Enum):
    SINGLE_PERSON_DISCOUNT = "single_person_discount"
    STUDENT_EXEMPTION = "student_exemption"
    EMPTY_PROPERTY = "empty_property"
    COUNCIL_TAX_REDUCTION = "council_tax_reduction"
    PROPERTY_BANDING = "property_banding"
    CUCKOOING = "cuckooing"
    
class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FraudIndicator:
    indicator_type: str
    description: str
    weight: float
    detected: bool = False
    evidence: Optional[str] = None

@dataclass
class FraudAssessment:
    case_id: str
    fraud_type: Optional[FraudType]
    risk_level: RiskLevel
    risk_score: float
    is_likely_fraud: bool
    is_likely_error: bool
    indicators: List[FraudIndicator]
    recommendations: List[str]
    confidence: float

class CouncilTaxFraudDetector:
    def __init__(self):
        self.fraud_patterns = self._initialize_fraud_patterns()
        self.error_patterns = self._initialize_error_patterns()
        self.risk_thresholds = {
            RiskLevel.LOW: 0.25,
            RiskLevel.MEDIUM: 0.50,
            RiskLevel.HIGH: 0.75,
            RiskLevel.CRITICAL: 0.90
        }
    
    def _initialize_fraud_patterns(self) -> Dict:
        return {
            FraudType.SINGLE_PERSON_DISCOUNT: [
                FraudIndicator("multiple_utility_accounts", "Multiple utility accounts in different names", 0.8),
                FraudIndicator("electoral_register_mismatch", "Electoral register shows multiple adults", 0.9),
                FraudIndicator("social_media_evidence", "Social media indicates cohabitation", 0.7),
                FraudIndicator("multiple_vehicles", "Multiple vehicles registered at property", 0.6),
                FraudIndicator("credit_check_mismatch", "Credit checks show multiple residents", 0.85),
            ],
            FraudType.STUDENT_EXEMPTION: [
                FraudIndicator("post_graduation_claim", "Claim continues after graduation date", 0.95),
                FraudIndicator("employment_income", "Employment records during claimed study", 0.9),
                FraudIndicator("part_time_status", "Part-time course claimed as full-time", 0.85),
                FraudIndicator("fake_documentation", "Suspected fraudulent enrollment docs", 0.98),
                FraudIndicator("historical_pattern", "Previous false student claims", 0.9),
            ],
            FraudType.EMPTY_PROPERTY: [
                FraudIndicator("utility_usage", "Utility usage in 'empty' property", 0.9),
                FraudIndicator("rental_listings", "Property on rental platforms", 0.95),
                FraudIndicator("neighbor_reports", "Neighbors report occupancy", 0.7),
                FraudIndicator("maintenance_activity", "Regular maintenance observed", 0.6),
                FraudIndicator("postal_deliveries", "Regular mail deliveries", 0.65),
            ],
            FraudType.CUCKOOING: [
                FraudIndicator("sudden_payment_regularity", "Sudden payment regularization", 0.8),
                FraudIndicator("behavior_change", "Significant property usage change", 0.85),
                FraudIndicator("antisocial_reports", "Increased antisocial behavior reports", 0.9),
                FraudIndicator("vulnerable_resident", "Resident is vulnerable person", 0.7),
                FraudIndicator("payment_source_change", "Unexplained payment source change", 0.75),
                FraudIndicator("police_intelligence", "Police intelligence indicators", 0.95),
            ],
        }
    
    def _initialize_error_patterns(self) -> List[FraudIndicator]:
        return [
            FraudIndicator("immediate_cooperation", "Immediate cooperation when contacted", -0.3),
            FraudIndicator("consistent_explanation", "Consistent explanations provided", -0.25),
            FraudIndicator("documentation_provided", "Willingly provides documentation", -0.2),
            FraudIndicator("self_reported", "Self-reported the change", -0.4),
            FraudIndicator("first_occurrence", "First time occurrence", -0.15),
            FraudIndicator("recent_life_change", "Recent bereavement/separation", -0.2),
        ]
    
    def detect_fraud(self, case_data: Dict) -> FraudAssessment:
        case_id = case_data.get('case_id', 'UNKNOWN')
        detected_indicators = []
        fraud_score = 0
        error_score = 0
        detected_fraud_type = None
        max_type_score = 0
        
        # Check each fraud type
        for fraud_type, indicators in self.fraud_patterns.items():
            type_score = 0
            type_indicators = []
            
            for indicator in indicators:
                if self._check_indicator(indicator, case_data):
                    indicator_copy = FraudIndicator(
                        indicator.indicator_type,
                        indicator.description,
                        indicator.weight,
                        True,
                        case_data.get(f'{indicator.indicator_type}_evidence', 'Detected in analysis')
                    )
                    type_indicators.append(indicator_copy)
                    type_score += indicator.weight
            
            if type_score > max_type_score:
                max_type_score = type_score
                detected_fraud_type = fraud_type
                detected_indicators = type_indicators
                fraud_score = min(type_score / len(indicators), 1.0) if indicators else 0
        
        # Check error patterns
        for error_indicator in self.error_patterns:
            if self._check_indicator(error_indicator, case_data):
                error_indicator_copy = FraudIndicator(
                    error_indicator.indicator_type,
                    error_indicator.description,
                    error_indicator.weight,
                    True,
                    "Mitigating factor detected"
                )
                detected_indicators.append(error_indicator_copy)
                error_score += abs(error_indicator.weight)
        
        # Calculate final risk score
        final_score = max(0, min(1, fraud_score - (error_score * 0.5)))
        
        # Determine risk level
        risk_level = self._calculate_risk_level(final_score)
        
        # Determine if fraud or error
        is_likely_fraud = final_score > 0.6 and error_score < 0.3
        is_likely_error = final_score < 0.4 or error_score > 0.5
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            detected_fraud_type, risk_level, is_likely_fraud, is_likely_error
        )
        
        # Calculate confidence
        confidence = min(0.95, (len(detected_indicators) / 10) + (final_score * 0.5))
        
        return FraudAssessment(
            case_id=case_id,
            fraud_type=detected_fraud_type,
            risk_level=risk_level,
            risk_score=final_score,
            is_likely_fraud=is_likely_fraud,
            is_likely_error=is_likely_error,
            indicators=detected_indicators,
            recommendations=recommendations,
            confidence=confidence
        )
    
    def _check_indicator(self, indicator: FraudIndicator, case_data: Dict) -> bool:
        # Simplified check - in production would use complex rules
        return case_data.get(indicator.indicator_type, False)
    
    def _calculate_risk_level(self, score: float) -> RiskLevel:
        if score >= self.risk_thresholds[RiskLevel.CRITICAL]:
            return RiskLevel.CRITICAL
        elif score >= self.risk_thresholds[RiskLevel.HIGH]:
            return RiskLevel.HIGH
        elif score >= self.risk_thresholds[RiskLevel.MEDIUM]:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_recommendations(self, fraud_type: Optional[FraudType], 
                                 risk_level: RiskLevel,
                                 is_likely_fraud: bool,
                                 is_likely_error: bool) -> List[str]:
        recommendations = []
        
        if is_likely_error:
            recommendations.append("Send educational letter about council tax obligations")
            recommendations.append("Offer support to correct the error")
        elif is_likely_fraud:
            if risk_level == RiskLevel.CRITICAL:
                recommendations.append("Immediate investigation required")
                recommendations.append("Consider prosecution if amount > £2000")
                recommendations.append("Issue formal caution")
            elif risk_level == RiskLevel.HIGH:
                recommendations.append("Schedule property inspection")
                recommendations.append("Request supporting documentation")
                recommendations.append("Cross-reference with other departments")
            elif risk_level == RiskLevel.MEDIUM:
                recommendations.append("Send compliance review letter")
                recommendations.append("Monitor account for 6 months")
            else:
                recommendations.append("Add to watchlist")
                recommendations.append("Review at next annual check")
        
        if fraud_type == FraudType.CUCKOOING:
            recommendations.insert(0, "Alert adult safeguarding team")
            recommendations.insert(1, "Coordinate with police")
        
        return recommendations
    
    def batch_analyze(self, cases: List[Dict]) -> Dict:
        results = []
        stats = {
            'total_cases': len(cases),
            'high_risk': 0,
            'likely_fraud': 0,
            'likely_error': 0,
            'by_type': {}
        }
        
        for case in cases:
            assessment = self.detect_fraud(case)
            results.append(assessment)
            
            if assessment.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                stats['high_risk'] += 1
            if assessment.is_likely_fraud:
                stats['likely_fraud'] += 1
            if assessment.is_likely_error:
                stats['likely_error'] += 1
            
            if assessment.fraud_type:
                fraud_type_str = assessment.fraud_type.value
                stats['by_type'][fraud_type_str] = stats['by_type'].get(fraud_type_str, 0) + 1
        
        return {
            'assessments': results,
            'statistics': stats
        }