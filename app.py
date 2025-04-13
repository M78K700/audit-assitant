import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import altair as alt
from pdf_generator import generate_pdf_download

# Configure the page with minimal settings
st.set_page_config(
    page_title="Financial Audit Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define sector-specific audit plans
SECTOR_AUDIT_PLANS = {
    "Technology": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review revenue recognition policies and practices",
            "Analyze expense management and cost controls"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Revenue recognition and billing systems",
            "Expense management and cost controls",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Revenue recognition", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Expense management", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Financial Services": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review compliance with financial regulations",
            "Analyze risk management frameworks"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Regulatory compliance",
            "Risk management systems",
            "Internal controls over financial reporting",
            "Transaction monitoring"
        ],
        "risks": {
            "High": ["Financial reporting accuracy", "Regulatory compliance", "Internal control weaknesses"],
            "Medium": ["Risk management", "Transaction monitoring", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Manufacturing": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review inventory valuation and management",
            "Analyze cost accounting systems"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Inventory management and valuation",
            "Cost accounting systems",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Inventory valuation", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Cost accounting", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Healthcare": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review revenue cycle management",
            "Analyze expense management and cost controls"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Revenue cycle management",
            "Expense management and cost controls",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Revenue recognition", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Expense management", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Retail": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review inventory valuation and management",
            "Analyze revenue recognition and sales reporting"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Inventory management and valuation",
            "Revenue recognition and sales reporting",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Inventory valuation", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Revenue recognition", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Energy": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review revenue recognition and pricing",
            "Analyze cost accounting and expense management"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Revenue recognition and pricing",
            "Cost accounting and expense management",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Revenue recognition", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Cost accounting", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Telecommunications": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review revenue recognition and billing systems",
            "Analyze expense management and cost controls"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Revenue recognition and billing systems",
            "Expense management and cost controls",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Revenue recognition", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Expense management", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Real Estate": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review property valuation and management",
            "Analyze revenue recognition and expense management"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Property valuation and management",
            "Revenue recognition and expense management",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Property valuation", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Revenue recognition", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    },
    "Education": {
        "objectives": [
            "Evaluate financial reporting accuracy and completeness",
            "Assess internal controls over financial reporting",
            "Review revenue recognition and tuition management",
            "Analyze expense management and cost controls"
        ],
        "scope": [
            "Financial statements and disclosures",
            "Revenue recognition and tuition management",
            "Expense management and cost controls",
            "Internal controls over financial reporting",
            "Tax compliance and reporting"
        ],
        "risks": {
            "High": ["Revenue recognition", "Financial reporting accuracy", "Internal control weaknesses"],
            "Medium": ["Expense management", "Tax compliance", "Financial disclosures"],
            "Low": ["Documentation", "Administrative processes", "IT systems"]
        }
    }
}

# Enhanced risk assessment criteria
RISK_ASSESSMENT_CRITERIA = {
    "High": {
        "Financial Impact": "Significant financial loss (>$1M)",
        "Regulatory Impact": "Major regulatory violations",
        "Reputation Impact": "Severe damage to reputation",
        "Operational Impact": "Critical system disruption",
        "Probability": "High likelihood of occurrence"
    },
    "Medium": {
        "Financial Impact": "Moderate financial loss ($100K-$1M)",
        "Regulatory Impact": "Minor regulatory violations",
        "Reputation Impact": "Moderate reputation damage",
        "Operational Impact": "Significant system disruption",
        "Probability": "Moderate likelihood of occurrence"
    },
    "Low": {
        "Financial Impact": "Minor financial loss (<$100K)",
        "Regulatory Impact": "Procedural non-compliance",
        "Reputation Impact": "Minimal reputation impact",
        "Operational Impact": "Limited system disruption",
        "Probability": "Low likelihood of occurrence"
    }
}

def main():
    st.title("Financial Audit Assistant 📊")
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Audit Planning", "Report Generation"]
    )
    
    if page == "Audit Planning":
        show_audit_planning()
    elif page == "Report Generation":
        show_report_generation()

def show_audit_planning():
    st.header("Financial Audit Planning")
    
    # Company Information Section
    st.header("Company Information")
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name")
        sector = st.selectbox(
            "Sector",
            list(SECTOR_AUDIT_PLANS.keys())
        )
    
    with col2:
        audit_start_date = st.date_input("Audit Start Date")
        audit_end_date = st.date_input("Audit End Date")
        team_size = st.number_input("Team Size", min_value=1, max_value=20, value=5)
    
    if company_name and sector:
        # Display Audit Plan
        st.header("Financial Audit Plan")
        
        # Objectives
        st.subheader("Audit Objectives")
        for objective in SECTOR_AUDIT_PLANS[sector]["objectives"]:
            st.markdown(f"- {objective}")
        
        # Scope
        st.subheader("Audit Scope")
        for scope_item in SECTOR_AUDIT_PLANS[sector]["scope"]:
            st.markdown(f"- {scope_item}")
        
        # Risk Assessment
        st.subheader("Risk Assessment")
        
        # High Risk Areas
        st.markdown("#### High Risk Areas")
        for risk in SECTOR_AUDIT_PLANS[sector]["risks"]["High"]:
            st.markdown(f"- {risk}")
        
        # Medium Risk Areas
        st.markdown("#### Medium Risk Areas")
        for risk in SECTOR_AUDIT_PLANS[sector]["risks"]["Medium"]:
            st.markdown(f"- {risk}")
        
        # Low Risk Areas
        st.markdown("#### Low Risk Areas")
        for risk in SECTOR_AUDIT_PLANS[sector]["risks"]["Low"]:
            st.markdown(f"- {risk}")
        
        # Resource Allocation
        st.subheader("Resource Allocation")
        
        # High Risk Team
        st.markdown("#### High Risk Team")
        high_risk_size = int(team_size * 0.5)
        high_risk_names = []
        for i in range(high_risk_size):
            name = st.text_input(f"Team Member {i+1} Name (High Risk)", key=f"high_risk_{i}")
            high_risk_names.append(name)
        
        # Medium Risk Team
        st.markdown("#### Medium Risk Team")
        medium_risk_size = int(team_size * 0.3)
        medium_risk_names = []
        for i in range(medium_risk_size):
            name = st.text_input(f"Team Member {i+1} Name (Medium Risk)", key=f"medium_risk_{i}")
            medium_risk_names.append(name)
        
        # Low Risk Team
        st.markdown("#### Low Risk Team")
        low_risk_size = int(team_size * 0.2)
        low_risk_names = []
        for i in range(low_risk_size):
            name = st.text_input(f"Team Member {i+1} Name (Low Risk)", key=f"low_risk_{i}")
            low_risk_names.append(name)
        
        # Generate Report Button
        st.markdown("---")
        st.subheader("Generate Audit Report")
        
        # Create audit plan dictionary for PDF generation
        audit_plan = {
            "company_name": company_name,
            "sector": sector,
            "audit_period": f"{audit_start_date.strftime('%B %d, %Y')} to {audit_end_date.strftime('%B %d, %Y')}",
            "team_size": team_size,
            "objectives": SECTOR_AUDIT_PLANS[sector]["objectives"],
            "scope": SECTOR_AUDIT_PLANS[sector]["scope"],
            "risks": SECTOR_AUDIT_PLANS[sector]["risks"],
            "team_members": {
                "high_risk": high_risk_names,
                "medium_risk": medium_risk_names,
                "low_risk": low_risk_names
            }
        }
        
        if st.button("Generate PDF Report"):
            try:
                pdf_bytes = generate_pdf_download(audit_plan)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"financial_audit_plan_{company_name.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
                st.success("Report generated successfully!")
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")

def show_report_generation():
    st.header("Financial Audit Report Generation")
    
    # Create a sample audit plan for demonstration
    sample_plan = {
        "company_name": "Sample Company",
        "sector": "Technology",
        "audit_period": "2024",
        "team_size": 5,
        "objectives": SECTOR_AUDIT_PLANS["Technology"]["objectives"],
        "scope": SECTOR_AUDIT_PLANS["Technology"]["scope"],
        "risks": SECTOR_AUDIT_PLANS["Technology"]["risks"]
    }
    
    if st.button("Generate PDF Report"):
        pdf_bytes = generate_pdf_download(sample_plan)
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="audit_report.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main() 