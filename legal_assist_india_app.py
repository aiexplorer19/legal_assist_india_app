import streamlit as st
import pandas as pd
import json
import os
import re
from datetime import datetime
import uuid
import base64
from streamlit_option_menu import option_menu
import sys
import streamlit as st






st.set_page_config(
    page_title="Legal Assist India",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Legal Assist India")


# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        font-size: 0.8rem;
        color: #4B5563;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .document-box {
        background-color: #EFF6FF;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 1px solid #BFDBFE;
    }
</style>
""", unsafe_allow_html=True)

# Load document templates
@st.cache_data
def load_document_templates():
    templates = {
        "Rental Agreement": {
            "template": """
# RENTAL AGREEMENT

THIS RENTAL AGREEMENT ("Agreement") is made and entered into on {date} by and between:

**LANDLORD**: {landlord_name}, residing at {landlord_address}, hereinafter referred to as the "LANDLORD"

AND

**TENANT**: {tenant_name}, residing at {tenant_address}, hereinafter referred to as the "TENANT"

## 1. PROPERTY
The Landlord agrees to rent to the Tenant the residential property located at: {property_address} ("the Premises").

## 2. TERM
This Agreement shall commence on {start_date} and continue for a period of {term_length} months, ending on {end_date}, unless terminated earlier as provided in this Agreement.

## 3. RENT
The Tenant agrees to pay rent of Rs. {monthly_rent} per month, payable in advance on or before the {rent_due_day}th day of each month. The first payment is due on {first_payment_date}.

## 4. SECURITY DEPOSIT
The Tenant shall pay a security deposit of Rs. {security_deposit} which will be refunded within 30 days after the termination of this Agreement, less any deductions for damages beyond normal wear and tear, unpaid rent, or other charges due.

## 5. UTILITIES
The responsibility for utilities shall be as follows:
- Electricity: {electricity_responsibility}
- Water: {water_responsibility}
- Internet: {internet_responsibility}
- Other utilities: {other_utilities}

## 6. MAINTENANCE AND REPAIRS
The Tenant shall maintain the Premises in a clean and sanitary condition and shall be responsible for repairs necessitated by Tenant's misuse. The Landlord shall be responsible for major repairs not caused by Tenant's negligence.

## 7. TERMINATION
Either party may terminate this Agreement at the end of the term by giving at least {notice_period} days' written notice. If no notice is given, the Agreement shall continue on a month-to-month basis with the same terms and conditions.

## 8. GOVERNING LAW
This Agreement shall be governed by the laws of India and the state of {state}.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

________________________
LANDLORD: {landlord_name}

________________________
TENANT: {tenant_name}
            """,
            "fields": [
                "landlord_name", "landlord_address", "tenant_name", "tenant_address", 
                "property_address", "start_date", "term_length", "end_date", "monthly_rent", 
                "rent_due_day", "first_payment_date", "security_deposit", "electricity_responsibility", 
                "water_responsibility", "internet_responsibility", "other_utilities", "notice_period", "state"
            ],
            "description": "A standard rental agreement for residential properties in India."
        },
        "Power of Attorney": {
            "template": """
# POWER OF ATTORNEY

**KNOW ALL MEN BY THESE PRESENTS:**

That I, {principal_name}, son/daughter of {principal_parent_name}, residing at {principal_address}, do hereby appoint and constitute {attorney_name}, son/daughter of {attorney_parent_name}, residing at {attorney_address}, as my true and lawful Attorney to act in my name and on my behalf to do the following acts, deeds and things in respect of the matters specified below:

## 1. PURPOSE AND POWERS
My Attorney shall have the authority to {purpose}, including but not limited to:
{specific_powers}

## 2. EFFECTIVE DATE AND DURATION
This Power of Attorney shall come into effect from {effective_date} and shall {duration_type}. {duration_details}

## 3. REVOCATION
I reserve the right to revoke this Power of Attorney at any time by providing written notice to my Attorney.

## 4. GOVERNING LAW
This Power of Attorney shall be governed by the laws of India.

IN WITNESS WHEREOF, I have signed this Power of Attorney on this {date} at {place}.

________________________
PRINCIPAL: {principal_name}

WITNESSES:
1. ________________________
   Name: {witness1_name}
   Address: {witness1_address}

2. ________________________
   Name: {witness2_name}
   Address: {witness2_address}
            """,
            "fields": [
                "principal_name", "principal_parent_name", "principal_address", 
                "attorney_name", "attorney_parent_name", "attorney_address",
                "purpose", "specific_powers", "effective_date", "duration_type", 
                "duration_details", "date", "place", "witness1_name", 
                "witness1_address", "witness2_name", "witness2_address"
            ],
            "description": "A Power of Attorney document authorizing someone to act on your behalf."
        },
        "Employment Contract": {
            "template": """
# EMPLOYMENT CONTRACT

THIS EMPLOYMENT CONTRACT ("Agreement") is made and entered into on {date} by and between:

**EMPLOYER**: {employer_name}, having its registered office at {employer_address}, represented by {employer_representative}, hereinafter referred to as the "EMPLOYER"

AND

**EMPLOYEE**: {employee_name}, residing at {employee_address}, hereinafter referred to as the "EMPLOYEE"

## 1. POSITION AND DUTIES
The Employer hereby employs the Employee as {job_title}. The Employee shall perform duties as described in the job description attached as Annexure A and such other duties as may be assigned from time to time.

## 2. TERM OF EMPLOYMENT
The employment shall commence on {start_date} and shall continue until terminated in accordance with this Agreement.

## 3. COMPENSATION
a) The Employee shall receive a basic salary of Rs. {basic_salary} per month.
b) Additional allowances: {allowances}
c) The salary shall be paid on or before the {salary_date} day of each month.

## 4. WORKING HOURS
The Employee shall work {working_hours} hours per week, from {working_days}.

## 5. LEAVE ENTITLEMENT
The Employee shall be entitled to:
a) {casual_leave} days of casual leave per year
b) {sick_leave} days of sick leave per year
c) {annual_leave} days of annual leave per year

## 6. PROBATION PERIOD
The Employee shall undergo a probation period of {probation_period} months, during which either party may terminate this Agreement with {probation_notice} days' notice.

## 7. NOTICE PERIOD
After completion of the probation period, either party may terminate this Agreement by giving {notice_period} days' written notice or payment in lieu thereof.

## 8. CONFIDENTIALITY
The Employee agrees to maintain confidentiality of all proprietary and confidential information of the Employer during and after the term of employment.

## 9. GOVERNING LAW
This Agreement shall be governed by the laws of India.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

________________________
EMPLOYER: {employer_representative}
For and on behalf of {employer_name}

________________________
EMPLOYEE: {employee_name}
            """,
            "fields": [
                "employer_name", "employer_address", "employer_representative", 
                "employee_name", "employee_address", "job_title", "start_date",
                "basic_salary", "allowances", "salary_date", "working_hours", 
                "working_days", "casual_leave", "sick_leave", "annual_leave",
                "probation_period", "probation_notice", "notice_period", "date"
            ],
            "description": "A standard employment contract for hiring employees in India."
        },
        "Promissory Note": {
            "template": """
# PROMISSORY NOTE

Rs. {loan_amount}                                                                                      Date: {date}
Place: {place}

FOR VALUE RECEIVED, I, {borrower_name}, son/daughter of {borrower_parent_name}, residing at {borrower_address} ("Borrower"), hereby unconditionally promise to pay to {lender_name}, son/daughter of {lender_parent_name}, residing at {lender_address} ("Lender"), or order, the principal sum of Rs. {loan_amount} (Rupees {loan_amount_words} only).

## 1. INTEREST RATE
This loan shall bear interest at the rate of {interest_rate}% per annum from the date of this Note until paid in full.

## 2. REPAYMENT TERMS
The principal and interest shall be payable in {repayment_schedule}. All payments shall be first applied to interest and then to principal.

## 3. PREPAYMENT
The Borrower may prepay this Note in whole or in part at any time without penalty.

## 4. DEFAULT
If any payment obligation under this Note is not paid when due, the entire principal amount and accrued interest shall become immediately due and payable at the option of the Lender.

## 5. GOVERNING LAW
This Note shall be governed by the laws of India.

IN WITNESS WHEREOF, the Borrower has executed this Promissory Note as of the date first above written.

________________________
BORROWER: {borrower_name}

WITNESSES:
1. ________________________
   Name: {witness1_name}
   Address: {witness1_address}

2. ________________________
   Name: {witness2_name}
   Address: {witness2_address}
            """,
            "fields": [
                "loan_amount", "date", "place", "borrower_name", "borrower_parent_name", 
                "borrower_address", "lender_name", "lender_parent_name", "lender_address", 
                "loan_amount_words", "interest_rate", "repayment_schedule", 
                "witness1_name", "witness1_address", "witness2_name", "witness2_address"
            ],
            "description": "A legally binding document where one party promises to pay a specific amount to another party."
        },
        "Affidavit": {
            "template": """
# AFFIDAVIT

I, {deponent_name}, son/daughter of {deponent_parent_name}, aged about {deponent_age} years, residing at {deponent_address}, do hereby solemnly affirm and declare as follows:

1. That I am the deponent in this affidavit and am fully competent to swear this affidavit.

2. {statement1}

3. {statement2}

4. {statement3}

5. That the contents of this affidavit are true and correct to the best of my knowledge and belief, and nothing material has been concealed therefrom.

VERIFICATION:

Verified at {place} on this {date} that the contents of the above affidavit are true and correct to the best of my knowledge and belief, and nothing material has been concealed therefrom.

________________________
DEPONENT: {deponent_name}

SWORN BEFORE ME:

________________________
NOTARY PUBLIC
            """,
            "fields": [
                "deponent_name", "deponent_parent_name", "deponent_age", "deponent_address", 
                "statement1", "statement2", "statement3", "place", "date"
            ],
            "description": "A written statement confirmed by oath or affirmation for use as evidence in court or other legal proceedings."
        },
        "Partnership Deed": {
            "template": """
# PARTNERSHIP DEED

THIS DEED OF PARTNERSHIP is made on this {date} at {place}, by and between:

1. {partner1_name}, son/daughter of {partner1_parent_name}, residing at {partner1_address} (hereinafter referred to as the "FIRST PARTY")

2. {partner2_name}, son/daughter of {partner2_parent_name}, residing at {partner2_address} (hereinafter referred to as the "SECOND PARTY")

3. {partner3_name}, son/daughter of {partner3_parent_name}, residing at {partner3_address} (hereinafter referred to as the "THIRD PARTY")

(The parties are hereinafter collectively referred to as the "PARTNERS")

WHEREAS the Partners have decided to start a business in partnership and have agreed to the following terms and conditions:

## 1. NAME AND BUSINESS
The Partners hereby form a partnership under the name and style of "{firm_name}" to carry on the business of {business_description}.

## 2. PLACE OF BUSINESS
The principal place of business of the partnership shall be at {business_address}, with the right to establish branches elsewhere as the Partners may from time to time decide.

## 3. COMMENCEMENT AND TERM
The partnership shall commence on {commencement_date} and shall continue until terminated as provided herein.

## 4. CAPITAL
The initial capital of the partnership shall be Rs. {total_capital}, which shall be contributed by the Partners in the following proportions:
- {partner1_name}: Rs. {partner1_capital} ({partner1_percentage}%)
- {partner2_name}: Rs. {partner2_capital} ({partner2_percentage}%)
- {partner3_name}: Rs. {partner3_capital} ({partner3_percentage}%)

## 5. PROFIT AND LOSS SHARING
The net profits and losses of the partnership shall be shared among the Partners in the following ratio:
- {partner1_name}: {partner1_profit_share}%
- {partner2_name}: {partner2_profit_share}%
- {partner3_name}: {partner3_profit_share}%

## 6. MANAGEMENT
All Partners shall have equal rights in the management of the partnership business. However, day-to-day decisions shall be made by majority vote of the Partners.

## 7. BANKING
The banking accounts of the partnership shall be maintained at {bank_name} and shall be operated by {account_operators}.

## 8. DISSOLUTION
The partnership may be dissolved by mutual consent of all Partners or as provided by the Indian Partnership Act, 1932.

IN WITNESS WHEREOF, the Partners have executed this Deed on the day and year first above written.

________________________
{partner1_name}

________________________
{partner2_name}

________________________
{partner3_name}

WITNESSES:
1. ________________________
   Name: {witness1_name}
   Address: {witness1_address}

2. ________________________
   Name: {witness2_name}
   Address: {witness2_address}
            """,
            "fields": [
                "date", "place", "partner1_name", "partner1_parent_name", "partner1_address", 
                "partner2_name", "partner2_parent_name", "partner2_address", 
                "partner3_name", "partner3_parent_name", "partner3_address", 
                "firm_name", "business_description", "business_address", "commencement_date", 
                "total_capital", "partner1_capital", "partner1_percentage", 
                "partner2_capital", "partner2_percentage", "partner3_capital", "partner3_percentage", 
                "partner1_profit_share", "partner2_profit_share", "partner3_profit_share", 
                "bank_name", "account_operators", "witness1_name", "witness1_address", 
                "witness2_name", "witness2_address"
            ],
            "description": "A legal document that outlines the terms and conditions of a partnership business."
        },
        "Will": {
            "template": """
# LAST WILL AND TESTAMENT

I, {testator_name}, son/daughter of {testator_parent_name}, residing at {testator_address}, being of sound mind and memory, do hereby make, publish, and declare this to be my Last Will and Testament, hereby revoking all Wills and Codicils heretofore made by me.

## 1. PERSONAL DETAILS
I declare that I am {marital_status}. {spouse_details}
{children_details}

## 2. APPOINTMENT OF EXECUTOR
I hereby appoint {executor_name}, residing at {executor_address}, to be the Executor of this my Last Will and Testament. In the event that {executor_name} is unable or unwilling to serve, then I appoint {alternate_executor} to be the Executor.

## 3. DISPOSITION OF PROPERTY
### 3.1 Immovable Property
{immovable_property_disposition}

### 3.2 Movable Property
{movable_property_disposition}

### 3.3 Bank Accounts and Investments
{financial_assets_disposition}

### 3.4 Residuary Estate
{residuary_disposition}

## 4. SPECIAL BEQUESTS
{special_bequests}

## 5. FUNERAL ARRANGEMENTS
{funeral_arrangements}

## 6. MISCELLANEOUS PROVISIONS
{miscellaneous_provisions}

IN WITNESS WHEREOF, I have hereunto set my hand to this my Last Will and Testament at {place} on this {date}.

________________________
TESTATOR: {testator_name}

SIGNED by the above-named Testator in our presence, who in our presence and in the presence of each other, all being present at the same time, have hereunto subscribed our names as witnesses:

WITNESSES:
1. ________________________
   Name: {witness1_name}
   Address: {witness1_address}

2. ________________________
   Name: {witness2_name}
   Address: {witness2_address}
            """,
            "fields": [
                "testator_name", "testator_parent_name", "testator_address", "marital_status", 
                "spouse_details", "children_details", "executor_name", "executor_address", 
                "alternate_executor", "immovable_property_disposition", "movable_property_disposition", 
                "financial_assets_disposition", "residuary_disposition", "special_bequests", 
                "funeral_arrangements", "miscellaneous_provisions", "place", "date", 
                "witness1_name", "witness1_address", "witness2_name", "witness2_address"
            ],
            "description": "A legal document that communicates a person's final wishes regarding their property and possessions after their death."
        }
    }
    return templates

# Load legal resources
@st.cache_data
def load_legal_resources():
    resources = {
        "Rental Laws": {
            "Rent Control Act": "The Rent Control Act regulates rent prices and eviction procedures in various states in India. Each state has its own version of the Act.",
            "Model Tenancy Act, 2021": "A central law that seeks to regulate rental housing by balancing the interests of both the landlord and tenant. It establishes rent authorities and tribunals for dispute resolution.",
            "Registration Act, 1908": "Requires registration of rental agreements exceeding 11 months at the sub-registrar's office.",
            "Key Provisions": [
                "Security deposit limitations vary by state (usually 2-3 months' rent)",
                "Rent increases must be as per agreement and state laws",
                "Maintenance responsibilities must be clearly defined",
                "Notice period for eviction is typically 1-3 months"
            ],
            "Common Issues": [
                "Disputes over security deposit refunds",
                "Unauthorized subletting",
                "Rent increases beyond permissible limits",
                "Eviction without proper notice"
            ]
        },
        "Power of Attorney Laws": {
            "Powers of Attorney Act, 1882": "This Act governs the creation and operation of Powers of Attorney in India.",
            "Registration Act, 1908": "Section 32 provides for registration of Powers of Attorney, though it's not mandatory except in certain cases involving immovable property.",
            "Key Provisions": [
                "Powers can be general or specific",
                "Can be revoked by the principal at any time",
                "For immovable property transactions, registration is recommended",
                "Expires automatically on the death or insanity of the principal"
            ],
            "Common Issues": [
                "Misuse of powers by the attorney",
                "Continuing to act after revocation",
                "Acting beyond the scope of authority",
                "Absence of witnesses"
            ]
        },
        "Employment Laws": {
            "Industrial Disputes Act, 1947": "Governs employer-employee relationships in industrial establishments.",
            "Factories Act, 1948": "Regulates working conditions in factories.",
            "Payment of Wages Act, 1936": "Ensures timely payment of wages to employees.",
            "Employees' Provident Funds Act, 1952": "Provides for retirement benefits.",
            "Payment of Gratuity Act, 1972": "Provides for gratuity payments to employees.",
            "Key Provisions": [
                "Maximum working hours (usually 48 hours per week)",
                "Minimum wage requirements as per state laws",
                "PF contributions (12% from employer and employee)",
                "Notice period requirements for termination",
                "Annual leave entitlements"
            ],
            "Common Issues": [
                "Non-payment of statutory benefits",
                "Arbitrary termination",
                "Excessive working hours",
                "Non-compliance with minimum wage laws"
            ]
        },
        "Loan Documentation": {
            "Indian Contract Act, 1872": "Governs contracts including loan agreements.",
            "Negotiable Instruments Act, 1881": "Governs promissory notes, cheques, etc.",
            "Registration Act, 1908": "For registration of mortgage documents.",
            "Key Provisions": [
                "Interest rates should be clearly specified",
                "Loan agreements exceeding certain amounts should be stamped",
                "Promissory notes should clearly state repayment terms",
                "Default clauses should be explicit"
            ],
            "Common Issues": [
                "Charging interest rates beyond legal limits",
                "Insufficient documentation",
                "Default on repayment",
                "Disputes over repayment schedules"
            ]
        },
        "Affidavits": {
            "Notaries Act, 1952": "Governs the appointment and functions of notaries who can attest affidavits.",
            "Indian Oaths Act, 1969": "Provides for administration of oaths for affidavits.",
            "Key Provisions": [
                "Must be sworn before a notary, magistrate, or other authorized person",
                "Must state that it is made solemnly, sincerely, and truly",
                "Must be signed by deponent",
                "False statements in affidavits can lead to prosecution for perjury"
            ],
            "Common Issues": [
                "Not properly sworn or attested",
                "Containing hearsay or irrelevant information",
                "Not based on personal knowledge",
                "Containing contradictory statements"
            ]
        },
        "Partnership Laws": {
            "Indian Partnership Act, 1932": "The primary law governing partnerships in India.",
            "Limited Liability Partnership Act, 2008": "Governs LLPs which combine features of companies and partnerships.",
            "Key Provisions": [
                "Partnership cannot exceed 20 partners (except for certain professions)",
                "Registration is optional but recommended",
                "Partners have unlimited liability",
                "Partners are agents of the firm and each other"
            ],
            "Common Issues": [
                "Disputes among partners",
                "Lack of clarity on profit/loss sharing",
                "Dissolution complications",
                "Absence of a written partnership deed"
            ]
        },
        "Succession Laws": {
            "Indian Succession Act, 1925": "Applies primarily to non-Hindus, governing testamentary succession.",
            "Hindu Succession Act, 1956": "Governs succession for Hindus, Buddhists, Jains, and Sikhs.",
            "Muslim Personal Law": "Governs succession for Muslims.",
            "Key Provisions": [
                "Will must be signed by testator and attested by two witnesses",
                "Testator must be of sound mind and not under coercion",
                "Religious personal laws may restrict testamentary freedom",
                "Laws of intestate succession vary by religion"
            ],
            "Common Issues": [
                "Will contests claiming undue influence",
                "Improper attestation",
                "Ambiguous bequests",
                "Claims from legal heirs not mentioned in will"
            ]
        }
    }
    return resources

# Function to save user data
def save_user_data(data):
    if 'user_documents' not in st.session_state:
        st.session_state.user_documents = []
    
    st.session_state.user_documents.append(data)

# Function to download document
def get_download_link(text, filename, display_text):
    """Generate a link to download the text file."""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{display_text}</a>'
    return href

# Function to generate a document from a template
def generate_document(template, field_values):
    document = template
    for key, value in field_values.items():
        document = document.replace("{" + key + "}", value)
    
    # Add current date if not explicitly provided
    if "{date}" in document:
        current_date = datetime.now().strftime("%d-%m-%Y")
        document = document.replace("{date}", current_date)
    
    return document

# Function to simplify legal language
def simplify_legal_language(text):
    # Dictionary of complex legal terms and their simplified versions
    simplifications = {
        r'\bhereby\b': 'by this document',
        r'\baforesaid\b': 'mentioned before',
        r'\bthereunder\b': 'under that',
        r'\bthereunto\b': 'to that',
        r'\bherein\b': 'in this document',
        r'\bthereof\b': 'of that',
        r'\bwhereas\b': 'because',
        r'\bnotwithstanding\b': 'despite',
        r'\bduly\b': 'properly',
        r'\bexecute\b': 'sign',
        r'\bterminate\b': 'end',
        r'\bcommence\b': 'begin',
        r'\bin witness whereof\b': 'as proof',
        r'\bfor and on behalf of\b': 'representing',
        r'\bin pursuance of\b': 'following',
        r'\bin accordance with\b': 'according to',
        r'\bpursuant to\b': 'according to',
        r'\bin respect of\b': 'regarding',
        r'\bfor the avoidance of doubt\b': 'to be clear',
        r'\bin the event that\b': 'if',
        r'\bat the discretion of\b': 'decided by',
        r'\bdeemed\b': 'considered',
        r'\bundertakes to\b': 'promises to',
        r'\bwithout prejudice to\b': 'not affecting',
        r'\bliable\b': 'responsible',
        r'\bshall\b': 'will',
        r'\bshall not\b': 'will not'
    }
    
    simplified_text = text
    for complex_term, simple_term in simplifications.items():
        simplified_text = re.sub(complex_term, simple_term, simplified_text, flags=re.IGNORECASE)
    
    return simplified_text

# Create the main navigation
def main():
    st.markdown('<h1 class="main-header">Legal Assist India</h1>', unsafe_allow_html=True)
    
    # Navigation menu
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995539.png", width=100)
        
        selected = option_menu(
            "Main Menu",
            ["Home", "Create Document", "Legal Resources", "Expert Advice", "My Documents"],
            icons=["house", "file-earmark-text", "book", "person-square", "folder"],
            menu_icon="list",
            default_index=0,
        )
    
    # Home page
    if selected == "Home":
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("## Welcome to Legal Assist India")
        st.markdown("""
        Legal Assist India is an AI-powered solution designed to simplify legal documentation for individuals and small businesses in India. Our platform makes it easy to create, understand, and manage legal documents.
        
        ### Key Features:
        - **Document Generation**: Create customized legal documents with simplified language
        - **Legal Resources**: Access information about Indian laws related to common legal documents
        - **Expert Advice**: Get guidance on legal matters from professionals
        - **Document Management**: Save and manage your legal documents securely
        
        Get started by selecting "Create Document" from the menu to generate your first legal document.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display sample documents
        st.markdown('<h2 class="sub-header">Available Document Templates</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### Rental Agreement
            A standardized lease agreement between landlord and tenant for residential properties.
            """)
            
            st.markdown("""
            #### Power of Attorney
            Authorize someone to act on your behalf for specified purposes.
            """)
        
        with col2:
            st.markdown("""
            #### Employment Contract
            Define the terms of employment between employer and employee.
            """)
            
            st.markdown("""
            #### Promissory Note
            A written promise to pay a specified sum to a person under certain terms.
            """)
        
        with col3:
            st.markdown("""
            #### Affidavit
            A sworn statement for use as evidence in legal proceedings.
            """)
            
            st.markdown("""
            #### Partnership Deed
            Establish the terms of a business partnership between two or more parties.
            """)
    
    # Create Document page
    elif selected == "Create Document":
        st.markdown('<h2 class="sub-header">Create Legal Document</h2>', unsafe_allow_html=True)
        
        templates = load_document_templates()
        
        # Document selection
        doc_type = st.selectbox("Select Document Type", list(templates.keys()))
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"### About {doc_type}")
        st.markdown(templates[doc_type]["description"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display form for selected document
        with st.form(key=f"{doc_type}_form"):
            st.subheader("Enter Document Details")
            
            # Get current date
            current_date = datetime.now().strftime("%d-%m-%Y")
            
            # Create form fields
            field_values = {}
            for field in templates[doc_type]["fields"]:
                if field == "date":
                    field_values[field] = st.text_input(f"{field.replace('_', ' ').title()}", value=current_date)
                else:
                    # Convert snake_case to Title Case for display
                    display_name = field.replace('_', ' ').title()
                    field_values[field] = st.text_input(display_name)
            
            # Simplification option
            simplify = st.checkbox("Simplify legal language")
            
            submit_button = st.form_submit_button(label="Generate Document")
        
        # Process form submission
        if submit_button:
            # Check if all required fields are filled
            if all(field_values.values()):
                document = generate_document(templates[doc_type]["template"], field_values)
                
                if simplify:
                    document = simplify_legal_language(document)
                
                # Save document to session state
                doc_id = str(uuid.uuid4())
                doc_data = {
                    "id": doc_id,
                    "type": doc_type,
                    "content": document,
                    "date_created": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "simplified": simplify
                }
                save_user_data(doc_data)
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("Document generated successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display the document
                st.markdown('<div class="document-box">', unsafe_allow_html=True)
                st.markdown("## Generated Document")
                st.markdown(document)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download button
                filename = f"{doc_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
                st.markdown(get_download_link(document, filename, "Download Document"), unsafe_allow_html=True)
            else:
                st.error("Please fill in all required fields.")
    
    # Legal Resources page
    elif selected == "Legal Resources":
        st.markdown('<h2 class="sub-header">Legal Resources</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        This section provides information on various laws and regulations in India related to common legal documents. 
        Select a category to learn more about the relevant laws, key provisions, and common issues.
        """)
        
        resources = load_legal_resources()
        
        resource_type = st.selectbox("Select Resource Category", list(resources.keys()))
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.subheader(f"{resource_type} in India")
        
        # Display relevant acts
        for act, description in resources[resource_type].items():
            if act not in ["Key Provisions", "Common Issues"]:
                st.markdown(f"#### {act}")
                st.markdown(description)
        
        # Display key provisions
        if "Key Provisions" in resources[resource_type]:
            st.markdown("#### Key Provisions")
            for provision in resources[resource_type]["Key Provisions"]:
                st.markdown(f"- {provision}")
        
        # Display common issues
        if "Common Issues" in resources[resource_type]:
            st.markdown("#### Common Issues")
            for issue in resources[resource_type]["Common Issues"]:
                st.markdown(f"- {issue}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Expert Advice page
    elif selected == "Expert Advice":
        st.markdown('<h2 class="sub-header">Expert Advice</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        Need personalized legal advice? Connect with a legal expert for consultation on your specific legal issues.
        
        **Note**: While our AI system can help create documents and provide general information, complex legal matters 
        should be handled by qualified legal professionals.
        """)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        
        # Expert advice form
        with st.form(key="expert_advice_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            
            # Legal areas
            legal_areas = [
                "Property Law", "Family Law", "Contract Law", "Corporate Law",
                "Employment Law", "Tax Law", "Criminal Law", "Other"
            ]
            area = st.selectbox("Area of Law", legal_areas)
            
            if area == "Other":
                other_area = st.text_input("Please specify")
            
            query = st.text_area("Describe your legal issue", height=150)
            
            urgency = st.selectbox("How urgent is your matter?", 
                                ["Not urgent", "Somewhat urgent", "Very urgent"])
            
            submit_query = st.form_submit_button("Submit Query")
        
        if submit_query:
            if name and email and query:
                st.success("Thank you for your query! A legal expert will contact you within 24-48 hours.")
                st.info("For urgent matters, please consider contacting a lawyer directly.")
            else:
                st.error("Please fill in all required fields (Name, Email, and Query).")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display legal experts info
        st.subheader("Our Legal Network")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Types of Experts in Our Network
            - **Lawyers** with expertise in various practice areas
            - **Legal Consultants** specialized in document review
            - **Paralegals** for assistance with documentation
            - **Notaries** for document attestation
            - **Mediators** for dispute resolution
            """)
        
        with col2:
            st.markdown("""
            #### Consultation Process
            1. Submit your query through the form
            2. Our team reviews your requirements
            3. We match you with an appropriate expert
            4. The expert contacts you for initial consultation
            5. You decide whether to proceed with their services
            """)
    
    # My Documents page
    elif selected == "My Documents":
        st.markdown('<h2 class="sub-header">My Documents</h2>', unsafe_allow_html=True)
        
        if 'user_documents' not in st.session_state or not st.session_state.user_documents:
            st.info("You haven't created any documents yet. Go to the 'Create Document' section to get started.")
        else:
            st.markdown("Here are your saved documents:")
            
            for i, doc in enumerate(st.session_state.user_documents):
                with st.expander(f"{doc['type']} (Created on {doc['date_created']})"):
                    st.markdown(doc['content'])
                    
                    # Download button
                    filename = f"{doc['type'].lower().replace(' ', '_')}_{i}.md"
                    st.markdown(get_download_link(doc['content'], filename, "Download Document"), unsafe_allow_html=True)
                    
                    # Delete button (functionality would require proper state management)
                    if st.button(f"Delete Document", key=f"del_{doc['id']}"):
                        st.session_state.user_documents.remove(doc)
                        st.experimental_rerun()
    
    # Footer
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown("© 2025 Legal Assist India | AI-Powered Legal Documentation Platform")
    st.markdown("Disclaimer: This tool provides general information and document templates. It is not a substitute for professional legal advice.")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()