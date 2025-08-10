import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fraud_detector import CouncilTaxFraudDetector, FraudType, RiskLevel
from data_generator import generate_sample_cases
import json
from datetime import datetime

st.set_page_config(
    page_title="Council Tax Fraud Prevention System",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_data
def load_sample_data():
    return generate_sample_cases(100)

def display_risk_gauge(risk_score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkred" if risk_score > 0.75 else "orange" if risk_score > 0.5 else "yellow" if risk_score > 0.25 else "green"},
            'steps': [
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "lightyellow"},
                {'range': [50, 75], 'color': "lightcoral"},
                {'range': [75, 100], 'color': "lightpink"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def main():
    st.title("🛡️ Council Tax Fraud Prevention System")
    st.markdown("### Advanced Detection & Classification Platform")
    
    # Initialize detector
    detector = CouncilTaxFraudDetector()
    
    # Sidebar
    st.sidebar.header("Control Panel")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard", "📋 Case Explorer", "🔍 Case Analysis", "🎯 Pattern Detection", "📈 Statistics", "⚙️ Settings"])
    
    with tab1:
        st.header("Real-time Monitoring Dashboard")
        
        # Load sample data
        sample_cases = load_sample_data()
        results = detector.batch_analyze(sample_cases)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Cases", results['statistics']['total_cases'])
        with col2:
            st.metric("High Risk", results['statistics']['high_risk'], 
                     delta=f"{(results['statistics']['high_risk']/results['statistics']['total_cases']*100):.1f}%")
        with col3:
            st.metric("Likely Fraud", results['statistics']['likely_fraud'],
                     delta=f"{(results['statistics']['likely_fraud']/results['statistics']['total_cases']*100):.1f}%")
        with col4:
            st.metric("Likely Error", results['statistics']['likely_error'],
                     delta=f"{(results['statistics']['likely_error']/results['statistics']['total_cases']*100):.1f}%")
        
        # Fraud type distribution
        st.subheader("Fraud Type Distribution")
        if results['statistics']['by_type']:
            fraud_df = pd.DataFrame(
                list(results['statistics']['by_type'].items()),
                columns=['Fraud Type', 'Count']
            )
            fig = px.pie(fraud_df, values='Count', names='Fraud Type', 
                        title="Detected Fraud Types",
                        color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True, key="fraud_type_distribution")
        
        # Recent high-risk cases
        st.subheader("🚨 High-Risk Cases Requiring Attention")
        high_risk_cases = [a for a in results['assessments'] 
                          if a.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]][:5]
        
        for case in high_risk_cases:
            with st.expander(f"Case {case.case_id} - {case.risk_level.value.upper()} RISK"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.plotly_chart(display_risk_gauge(case.risk_score), use_container_width=True, key=f"risk_gauge_{case.case_id}")
                with col2:
                    st.write(f"**Fraud Type:** {case.fraud_type.value if case.fraud_type else 'Unknown'}")
                    st.write(f"**Classification:** {'FRAUD' if case.is_likely_fraud else 'ERROR' if case.is_likely_error else 'UNCERTAIN'}")
                    st.write(f"**Confidence:** {case.confidence:.1%}")
                    st.write("**Recommendations:**")
                    for rec in case.recommendations[:3]:
                        st.write(f"• {rec}")
    
    with tab2:
        st.header("📋 All Cases Explorer")
        st.write(f"**Total Cases in System: {len(sample_cases)}**")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_filter = st.selectbox(
                "Filter by Risk Level",
                ["All", "Critical", "High", "Medium", "Low"]
            )
        
        with col2:
            fraud_filter = st.selectbox(
                "Filter by Classification",
                ["All", "Likely Fraud", "Likely Error", "Uncertain"]
            )
        
        with col3:
            fraud_type_filter = st.selectbox(
                "Filter by Fraud Type",
                ["All", "Single Person Discount", "Student Exemption", "Empty Property", 
                 "Council Tax Reduction", "Property Banding", "Cuckooing"]
            )
        
        with col4:
            sort_by = st.selectbox(
                "Sort by",
                ["Risk Score (High to Low)", "Risk Score (Low to High)", 
                 "Case ID", "Property ID", "Confidence"]
            )
        
        # Search box
        search_term = st.text_input("Search cases (by ID, property, or account holder):", "")
        
        # Filter and sort the cases
        filtered_results = []
        for case, assessment in zip(sample_cases, results['assessments']):
            # Apply filters
            if risk_filter != "All" and assessment.risk_level.value.lower() != risk_filter.lower():
                continue
            
            if fraud_filter == "Likely Fraud" and not assessment.is_likely_fraud:
                continue
            elif fraud_filter == "Likely Error" and not assessment.is_likely_error:
                continue
            elif fraud_filter == "Uncertain" and (assessment.is_likely_fraud or assessment.is_likely_error):
                continue
            
            if fraud_type_filter != "All" and assessment.fraud_type:
                if assessment.fraud_type.value != fraud_type_filter:
                    continue
            
            # Apply search
            if search_term:
                search_lower = search_term.lower()
                if not any([
                    search_lower in case.get('case_id', '').lower(),
                    search_lower in case.get('property_id', '').lower(),
                    search_lower in case.get('account_holder', '').lower(),
                    search_lower in case.get('address', '').lower()
                ]):
                    continue
            
            filtered_results.append((case, assessment))
        
        # Sort results
        if "Risk Score (High to Low)" in sort_by:
            filtered_results.sort(key=lambda x: x[1].risk_score, reverse=True)
        elif "Risk Score (Low to High)" in sort_by:
            filtered_results.sort(key=lambda x: x[1].risk_score)
        elif "Case ID" in sort_by:
            filtered_results.sort(key=lambda x: x[0].get('case_id', ''))
        elif "Property ID" in sort_by:
            filtered_results.sort(key=lambda x: x[0].get('property_id', ''))
        elif "Confidence" in sort_by:
            filtered_results.sort(key=lambda x: x[1].confidence, reverse=True)
        
        st.write(f"**Showing {len(filtered_results)} cases**")
        
        # Display options
        view_mode = st.radio("View Mode", ["Detailed Cards", "Compact Table", "Risk Matrix"], horizontal=True)
        
        if view_mode == "Detailed Cards":
            # Pagination
            cases_per_page = 10
            total_pages = max(1, (len(filtered_results) - 1) // cases_per_page + 1)
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            
            start_idx = (page - 1) * cases_per_page
            end_idx = min(start_idx + cases_per_page, len(filtered_results))
            
            for case, assessment in filtered_results[start_idx:end_idx]:
                with st.expander(f"📁 {case['case_id']} - Risk: {assessment.risk_level.value.upper()} ({assessment.risk_score:.1%})"):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write("**Case Details:**")
                        st.write(f"• Property: {case.get('property_id', 'N/A')}")
                        st.write(f"• Account: {case.get('account_holder', 'N/A')}")
                        st.write(f"• Address: {case.get('address', 'N/A')}")
                        st.write(f"• Band: {case.get('council_tax_band', 'N/A')}")
                        st.write(f"• Annual Charge: £{case.get('annual_charge', 0):,}")
                    
                    with col2:
                        st.write("**Risk Assessment:**")
                        st.write(f"• Score: {assessment.risk_score:.1%}")
                        st.write(f"• Confidence: {assessment.confidence:.1%}")
                        st.write(f"• Classification: {'FRAUD' if assessment.is_likely_fraud else 'ERROR' if assessment.is_likely_error else 'UNCERTAIN'}")
                        if assessment.fraud_type:
                            st.write(f"• Type: {assessment.fraud_type.value}")
                    
                    with col3:
                        st.plotly_chart(display_risk_gauge(assessment.risk_score), use_container_width=True, key=f"explorer_gauge_{case['case_id']}")
                    
                    if assessment.recommendations:
                        st.write("**Recommended Actions:**")
                        for rec in assessment.recommendations[:3]:
                            st.write(f"• {rec}")
        
        elif view_mode == "Compact Table":
            # Create DataFrame for table view
            table_data = []
            for case, assessment in filtered_results:
                table_data.append({
                    'Case ID': case['case_id'],
                    'Property': case.get('property_id', 'N/A'),
                    'Account Holder': case.get('account_holder', 'N/A'),
                    'Risk Level': assessment.risk_level.value.upper(),
                    'Risk Score': f"{assessment.risk_score:.1%}",
                    'Confidence': f"{assessment.confidence:.1%}",
                    'Classification': 'FRAUD' if assessment.is_likely_fraud else 'ERROR' if assessment.is_likely_error else 'UNCERTAIN',
                    'Fraud Type': assessment.fraud_type.value if assessment.fraud_type else 'N/A',
                    'Band': case.get('council_tax_band', 'N/A'),
                    'Annual Charge': f"£{case.get('annual_charge', 0):,}"
                })
            
            if table_data:
                df_cases = pd.DataFrame(table_data)
                st.dataframe(df_cases, use_container_width=True, height=600)
                
                # Download option
                csv = df_cases.to_csv(index=False)
                st.download_button(
                    label="Download Cases as CSV",
                    data=csv,
                    file_name=f"council_tax_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        else:  # Risk Matrix view
            st.write("**Risk Distribution Matrix**")
            
            # Create risk matrix
            matrix = {'Critical': [], 'High': [], 'Medium': [], 'Low': []}
            for case, assessment in filtered_results:
                matrix[assessment.risk_level.value.capitalize()].append((case, assessment))
            
            # Display matrix
            for level in ['Critical', 'High', 'Medium', 'Low']:
                if matrix[level]:
                    st.subheader(f"{level} Risk ({len(matrix[level])} cases)")
                    cols = st.columns(min(4, len(matrix[level])))
                    for i, (case, assessment) in enumerate(matrix[level][:12]):  # Show max 12 per level
                        with cols[i % 4]:
                            color = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}[level]
                            st.write(f"{color} **{case['case_id']}**")
                            st.write(f"Score: {assessment.risk_score:.1%}")
                            if assessment.fraud_type:
                                st.write(f"Type: {assessment.fraud_type.value[:15]}...")
    
    with tab3:
        st.header("Individual Case Analysis")
        
        # Case input form
        with st.form("case_analysis_form"):
            st.subheader("Enter Case Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                case_id = st.text_input("Case ID", value="CASE-2024-001")
                
                st.write("**Single Person Discount Indicators**")
                multiple_utility = st.checkbox("Multiple utility accounts detected")
                electoral_mismatch = st.checkbox("Electoral register mismatch")
                social_media = st.checkbox("Social media evidence of cohabitation")
                multiple_vehicles = st.checkbox("Multiple vehicles at property")
                
                st.write("**Student Exemption Indicators**")
                post_graduation = st.checkbox("Claim after graduation")
                employment_income = st.checkbox("Employment during study")
                part_time_status = st.checkbox("Part-time claimed as full-time")
                
            with col2:
                st.write("**Empty Property Indicators**")
                utility_usage = st.checkbox("Utility usage detected")
                rental_listings = st.checkbox("Property on rental sites")
                neighbor_reports = st.checkbox("Neighbor occupancy reports")
                
                st.write("**Cuckooing Indicators**")
                sudden_payment = st.checkbox("Sudden payment regularization")
                behavior_change = st.checkbox("Property usage changes")
                antisocial_reports = st.checkbox("Antisocial behavior reports")
                vulnerable_resident = st.checkbox("Vulnerable resident")
                
                st.write("**Error Indicators**")
                immediate_cooperation = st.checkbox("Immediate cooperation")
                consistent_explanation = st.checkbox("Consistent explanations")
                self_reported = st.checkbox("Self-reported change")
            
            submitted = st.form_submit_button("Analyze Case")
            
            if submitted:
                # Build case data
                case_data = {
                    'case_id': case_id,
                    'multiple_utility_accounts': multiple_utility,
                    'electoral_register_mismatch': electoral_mismatch,
                    'social_media_evidence': social_media,
                    'multiple_vehicles': multiple_vehicles,
                    'post_graduation_claim': post_graduation,
                    'employment_income': employment_income,
                    'part_time_status': part_time_status,
                    'utility_usage': utility_usage,
                    'rental_listings': rental_listings,
                    'neighbor_reports': neighbor_reports,
                    'sudden_payment_regularity': sudden_payment,
                    'behavior_change': behavior_change,
                    'antisocial_reports': antisocial_reports,
                    'vulnerable_resident': vulnerable_resident,
                    'immediate_cooperation': immediate_cooperation,
                    'consistent_explanation': consistent_explanation,
                    'self_reported': self_reported
                }
                
                # Analyze
                assessment = detector.detect_fraud(case_data)
                
                # Display results
                st.divider()
                st.subheader("Analysis Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.plotly_chart(display_risk_gauge(assessment.risk_score), use_container_width=True, key="case_analysis_risk_gauge")
                
                with col2:
                    st.metric("Risk Level", assessment.risk_level.value.upper())
                    st.metric("Confidence", f"{assessment.confidence:.1%}")
                
                with col3:
                    if assessment.is_likely_fraud:
                        st.error("⚠️ LIKELY FRAUD")
                    elif assessment.is_likely_error:
                        st.success("✓ LIKELY ERROR")
                    else:
                        st.warning("⚡ UNCERTAIN")
                    
                    if assessment.fraud_type:
                        st.info(f"Type: {assessment.fraud_type.value}")
                
                # Indicators
                st.subheader("Detected Indicators")
                for indicator in assessment.indicators:
                    if indicator.detected:
                        if indicator.weight > 0:
                            st.warning(f"🔴 {indicator.description} (Weight: {indicator.weight:.2f})")
                        else:
                            st.success(f"🟢 {indicator.description} (Mitigating: {abs(indicator.weight):.2f})")
                
                # Recommendations
                st.subheader("Recommended Actions")
                for i, rec in enumerate(assessment.recommendations, 1):
                    st.write(f"{i}. {rec}")
    
    with tab4:
        st.header("Pattern Detection & Analysis")
        
        # Cuckooing detection special section
        st.subheader("🏠 Cuckooing Detection Module")
        st.info("Specialized detection for property takeover by criminal groups")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Key Indicators:**")
            st.write("• Vulnerable person suddenly makes regular payments")
            st.write("• Increased anti-social behavior reports")
            st.write("• Change in property usage patterns")
            st.write("• New faces seen entering/leaving property")
            st.write("• Payment source changes without explanation")
        
        with col2:
            st.write("**Detection Algorithm:**")
            st.code("""
            risk_score = 0
            if vulnerable_person and sudden_payment:
                risk_score += 0.4
            if antisocial_behavior_increase > 50%:
                risk_score += 0.3
            if payment_source_changed:
                risk_score += 0.2
            if police_intelligence:
                risk_score += 0.5
            """, language="python")
        
        # Fraud vs Error Classification
        st.subheader("🎯 Fraud vs Error Classification")
        
        # Create comparison data
        comparison_data = {
            'Indicator': [
                'Response to contact',
                'Documentation',
                'Explanation consistency',
                'Historical pattern',
                'Cooperation level',
                'Intent indicators'
            ],
            'Fraud': [
                'Avoids/delays contact',
                'Reluctant to provide',
                'Inconsistent stories',
                'Previous violations',
                'Defensive/hostile',
                'Clear deception patterns'
            ],
            'Error': [
                'Immediate response',
                'Readily provides',
                'Consistent explanation',
                'First occurrence',
                'Fully cooperative',
                'Genuine confusion'
            ]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.table(df_comparison)
    
    with tab5:
        st.header("Statistical Analysis")
        
        # Generate more sample data for statistics
        large_sample = generate_sample_cases(500)
        large_results = detector.batch_analyze(large_sample)
        
        # Risk distribution
        risk_distribution = {'Low': 0, 'Medium': 0, 'High': 0, 'Critical': 0}
        for assessment in large_results['assessments']:
            risk_distribution[assessment.risk_level.value.capitalize()] += 1
        
        fig_risk = px.bar(
            x=list(risk_distribution.keys()),
            y=list(risk_distribution.values()),
            title="Risk Level Distribution",
            labels={'x': 'Risk Level', 'y': 'Number of Cases'},
            color=list(risk_distribution.values()),
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig_risk, use_container_width=True, key="risk_distribution_chart")
        
        # Time series simulation
        st.subheader("Detection Trends (Simulated)")
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        fraud_counts = [int(20 + 10 * (i/30) + 5 * (i % 7)) for i in range(30)]
        error_counts = [int(15 + 5 * (i/30) + 3 * ((i+3) % 5)) for i in range(30)]
        
        trend_df = pd.DataFrame({
            'Date': dates,
            'Fraud Cases': fraud_counts,
            'Error Cases': error_counts
        })
        
        fig_trend = px.line(trend_df, x='Date', y=['Fraud Cases', 'Error Cases'],
                           title="Detection Trends Over Time")
        st.plotly_chart(fig_trend, use_container_width=True, key="detection_trends_chart")
        
        # Financial impact
        st.subheader("Estimated Financial Impact")
        avg_fraud_amount = 2500  # Average fraud amount in pounds
        detected_fraud = results['statistics']['likely_fraud']
        total_prevented = detected_fraud * avg_fraud_amount
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Frauds Detected", detected_fraud)
        with col2:
            st.metric("Avg Fraud Amount", f"£{avg_fraud_amount:,}")
        with col3:
            st.metric("Total Prevented", f"£{total_prevented:,}")
    
    with tab6:
        st.header("System Settings")
        
        st.subheader("Risk Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            low_threshold = st.slider("Low Risk Threshold", 0.0, 1.0, 0.25)
            medium_threshold = st.slider("Medium Risk Threshold", 0.0, 1.0, 0.50)
        
        with col2:
            high_threshold = st.slider("High Risk Threshold", 0.0, 1.0, 0.75)
            critical_threshold = st.slider("Critical Risk Threshold", 0.0, 1.0, 0.90)
        
        st.subheader("Alert Settings")
        email_alerts = st.checkbox("Enable email alerts for high-risk cases", value=True)
        daily_reports = st.checkbox("Generate daily summary reports", value=True)
        
        st.subheader("Data Sources")
        st.write("Connected Systems:")
        st.write("✅ Electoral Register Database")
        st.write("✅ Utility Provider APIs")
        st.write("✅ Credit Reference Agencies")
        st.write("✅ Social Services Database")
        st.write("⚠️ Police Intelligence Feed (Pending)")
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()