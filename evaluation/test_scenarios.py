"""
test_scenarios.py
-----------------
10 unique evaluation scenarios:
  - intent       : The core purpose of the email
  - key_facts    : Bullet points that MUST appear in the email
  - tone         : Desired communication style
  - reference    : Human-written ideal email for comparison

Each scenario tests a distinct professional communication context.
"""

SCENARIOS = [
    # ─────────────────────────────────────────────────────────────────────
    # Scenario 1 — Post-interview follow-up
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 1,
        "intent": "Follow up after a job interview",
        "key_facts": [
            "Interviewed on Tuesday for the Product Manager role at Axiom Labs",
            "Discussed roadmap planning using the OKR framework",
            "Available to start within two weeks",
            "Interviewer was Sarah Chen, Head of Product",
        ],
        "tone": "Professional",
        "reference": """Subject: Follow-Up: Product Manager Interview – [Your Name]

Dear Sarah,

Thank you for meeting with me on Tuesday to discuss the Product Manager role at Axiom Labs. I genuinely enjoyed our conversation about using the OKR framework for roadmap planning — it aligned closely with my experience structuring cross-functional priorities.

I remain very enthusiastic about this opportunity and wanted to confirm that I am available to start within two weeks should an offer be extended. Please let me know if there is any further information I can provide.

I look forward to hearing from you.

Best regards,
[Your Name]""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 2 — Vendor proposal request
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 2,
        "intent": "Request proposal details from a vendor",
        "key_facts": [
            "Vendor is CloudNest Solutions",
            "Requesting pricing for 200 cloud storage licenses (Enterprise tier)",
            "Need SLA documentation and onboarding timeline",
            "Proposal deadline is June 15th",
        ],
        "tone": "Formal",
        "reference": """Subject: Request for Proposal – Enterprise Cloud Storage Licenses

Dear CloudNest Solutions Team,

I am writing on behalf of our IT procurement department to formally request a detailed proposal for 200 Enterprise-tier cloud storage licenses. In addition to per-unit pricing and available volume discounts, please include your standard SLA documentation and a proposed onboarding timeline.

Kindly ensure that all proposal materials are submitted by June 15th to align with our procurement review cycle.

For any clarifications, please do not hesitate to contact our office directly. We look forward to your response.

Yours sincerely,
[Your Name]
IT Procurement Department""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 3 — Missed deadline apology
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 3,
        "intent": "Apologize for missing a project deadline",
        "key_facts": [
            "The Q3 financial report was due last Friday",
            "Delay caused by unexpected data migration issues",
            "Report will be delivered by Wednesday EOD",
            "Steps taken to prevent recurrence: added automated data validation checks",
        ],
        "tone": "Empathetic",
        "reference": """Subject: Apology for Delay – Q3 Financial Report

Dear [Manager's Name],

I want to sincerely apologize for failing to deliver the Q3 financial report by last Friday's deadline. I understand that this may have caused inconvenience, and I take full responsibility for the delay.

The root cause was an unexpected data migration issue that disrupted our reporting pipeline. I have since implemented automated data validation checks to ensure this does not recur, and I am committed to delivering the completed report by Wednesday EOD.

Thank you for your patience and understanding. Please let me know if there is anything else I can do to support the team during this delay.

Warm regards,
[Your Name]""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 4 — New team member introduction
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 4,
        "intent": "Introduce a new team member to the company",
        "key_facts": [
            "New hire is Priya Sharma, joining as Lead UX Designer",
            "She starts on Monday, April 21st",
            "Comes from a background at Flipkart and Zomato",
            "She will be based in the Bangalore office",
        ],
        "tone": "Friendly",
        "reference": """Subject: Welcome Priya Sharma – Our New Lead UX Designer!

Hi Team,

I am delighted to introduce Priya Sharma, who will be joining us as our new Lead UX Designer starting Monday, April 21st!

Priya brings a wealth of experience from her time at Flipkart and Zomato, where she led user research and design systems at scale. She will be based in our Bangalore office and is excited to connect with everyone.

Please join me in giving Priya a warm welcome — feel free to drop by and say hello on Monday!

Best,
[Your Name]""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 5 — Declining a meeting invitation
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 5,
        "intent": "Decline a meeting invitation politely",
        "key_facts": [
            "Meeting is the Thursday panel discussion on AI Ethics",
            "Unable to attend due to a prior client commitment",
            "Happy to share written thoughts on the topic instead",
            "Available for a follow-up call the following week",
        ],
        "tone": "Diplomatic",
        "reference": """Subject: Re: Thursday AI Ethics Panel – Unable to Attend

Dear [Organizer's Name],

Thank you for the kind invitation to Thursday's panel discussion on AI Ethics. Unfortunately, I have a prior client commitment that I am unable to reschedule, and I will not be able to attend.

I would be happy to contribute written thoughts on the topic if that would be useful for the panel. Additionally, I am available for a follow-up conversation the following week should you wish to discuss further.

I hope the discussion is a great success and look forward to hearing about the key takeaways.

Kind regards,
[Your Name]""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 6 — Salary review request
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 6,
        "intent": "Request a salary review from a manager",
        "key_facts": [
            "Have been in the current role for 2.5 years without a salary adjustment",
            "Successfully led the migration to AWS, saving the company $120,000 annually",
            "Current salary is below the market median for this role based on industry surveys",
            "Requesting a 15% increase",
        ],
        "tone": "Confident",
        "reference": """Subject: Request for Salary Review

Dear [Manager's Name],

I am writing to formally request a review of my current compensation. Over the past 2.5 years in this role, I have consistently delivered high-impact results — most notably, leading the AWS migration project that generated $120,000 in annual savings for the company.

After reviewing current industry benchmarks, I have found that my compensation is below the market median for this position and level of responsibility. With this context in mind, I would like to request a 15% salary increase to bring my compensation in line with market standards.

I would welcome the opportunity to discuss this further at your earliest convenience. Thank you for your time and consideration.

Best regards,
[Your Name]""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 7 — Unpaid invoice follow-up
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 7,
        "intent": "Follow up on an unpaid invoice",
        "key_facts": [
            "Invoice #INV-2024-089 for $4,750 was due on March 31st",
            "Two previous reminders sent on April 5th and April 12th",
            "Payment must be received by April 20th to avoid a 2% late fee",
            "Client is Meridian Consulting",
        ],
        "tone": "Firm and Urgent",
        "reference": """Subject: URGENT: Overdue Invoice #INV-2024-089 – Action Required

Dear Meridian Consulting Accounts Team,

This is a final reminder regarding Invoice #INV-2024-089 for the amount of $4,750, which was due on March 31st. Despite reminders sent on April 5th and April 12th, we have not yet received payment.

Please be advised that payment must be received by April 20th. Any balance remaining after this date will be subject to a 2% late fee in accordance with our payment terms.

We value our relationship with Meridian Consulting and hope to resolve this matter promptly. Please confirm receipt of this notice or contact us immediately if there is an issue.

Regards,
[Your Name]
Accounts Receivable""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 8 — Post-project thank you to client
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 8,
        "intent": "Thank a client after completing a project",
        "key_facts": [
            "Project was the redesign of Vertex Corp's e-commerce platform",
            "Project completed 1 week ahead of schedule",
            "Client's team was collaborative and responsive throughout",
            "Hopeful for a long-term partnership",
        ],
        "tone": "Warm and Grateful",
        "reference": """Subject: Thank You – Vertex Corp E-Commerce Redesign

Dear [Client's Name],

Now that the dust has settled on the successful completion of the Vertex Corp e-commerce platform redesign, I wanted to take a moment to personally thank you and your team for an outstanding collaboration.

The project was delivered a full week ahead of schedule, which is a testament to how responsive and engaged your team was at every stage. Working with such a dedicated client made the entire process genuinely enjoyable.

We are proud of what we built together and sincerely hope this marks the beginning of a long-term partnership. Please do not hesitate to reach out whenever we can be of service.

With appreciation,
[Your Name]""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 9 — Product pitch to potential client
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 9,
        "intent": "Pitch a product to a potential client",
        "key_facts": [
            "Product is DataPulse — an AI-powered analytics dashboard",
            "Reduces reporting time by 60% on average",
            "Used by over 300 companies including Fortune 500 firms",
            "Offering a free 30-day trial with no credit card required",
        ],
        "tone": "Persuasive",
        "reference": """Subject: Cut Your Reporting Time by 60% – Introducing DataPulse

Dear [Prospect's Name],

I hope this message finds you well. I wanted to introduce you to DataPulse, an AI-powered analytics dashboard that is transforming how leading organizations handle their data.

On average, our clients reduce reporting time by 60% — freeing up their teams to focus on insights rather than data wrangling. DataPulse is trusted by over 300 companies, including several Fortune 500 firms, across industries.

We would love to show you what DataPulse can do for your team. To make this easy, we are offering a fully featured 30-day free trial — no credit card required.

Would you be open to a 20-minute demo call this week? I am confident you will see immediate value.

Best regards,
[Your Name]""",
    },

    # ─────────────────────────────────────────────────────────────────────
    # Scenario 10 — Customer support escalation
    # ─────────────────────────────────────────────────────────────────────
    {
        "id": 10,
        "intent": "Escalate an unresolved customer support issue",
        "key_facts": [
            "Support ticket #TKT-55821 opened 12 days ago",
            "Issue: complete payment gateway failure on the production API",
            "Business is losing approximately $8,000 per day due to this outage",
            "Previous support agents provided no resolution",
            "Requesting escalation to a senior engineer immediately",
        ],
        "tone": "Urgent and Assertive",
        "reference": """Subject: ESCALATION REQUIRED: Critical Payment Gateway Outage – Ticket #TKT-55821

Dear Support Leadership Team,

I am writing to formally escalate Ticket #TKT-55821, opened 12 days ago, which remains completely unresolved. This issue involves a critical failure of the production payment gateway API that is costing our business approximately $8,000 per day in lost revenue.

Despite multiple interactions with your support team, no actionable resolution has been provided. This is no longer acceptable given the severity and financial impact of the outage.

I am requesting the immediate assignment of a senior engineer to this case. We need a confirmed timeline for resolution within 24 hours.

Please treat this as a critical priority. I am available immediately for a call or screen share.

Regards,
[Your Name]""",
    },
]
