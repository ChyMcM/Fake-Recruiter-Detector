# scoring.py - Rule-based scoring engine for recruiter message analysis

from typing import Dict, List, Tuple

# Each entry maps a suspicious keyword/phrase to a (score_weight, flag_description) tuple.
# Organized by category: Payment Methods, Communication Channels, Job Red Flags, 
# Personal Info Requests, Urgency/Pressure, Unrealistic Claims, and Other Scam Indicators
SUSPICIOUS_PATTERNS: Dict[str, Tuple[int, str]] = {
    # --- PAYMENT METHODS (High Risk) ---
    "gift card": (30, "Requests payment via gift card"),
    "crypto": (25, "Mentions cryptocurrency payment"),
    "bitcoin": (25, "Mentions Bitcoin payment"),
    "ethereum": (25, "Mentions Ethereum payment"),
    "wire transfer": (25, "Requests wire transfer"),
    "western union": (30, "Mentions Western Union"),
    "money gram": (30, "Mentions MoneyGram transfer"),
    "bank transfer": (20, "Requests bank transfer"),
    "paypal": (15, "Requests PayPal payment"),
    "amazon gift": (30, "Requests Amazon gift card"),
    "itunes": (30, "Mentions iTunes gift card"),
    "fee": (20, "Mentions upfront fee"),
    "advance payment": (25, "Requests advance payment"),
    "processing fee": (28, "Mentions processing/setup fee"),
    "initial investment": (25, "Requires initial investment"),
    "security deposit": (25, "Requests security deposit"),

    # --- OFF-PLATFORM COMMUNICATION (Medium-High Risk) ---
    "telegram": (20, "Asks to move conversation to Telegram"),
    "whatsapp": (15, "Asks to move to WhatsApp"),
    "signal": (15, "Asks to move to Signal"),
    "viber": (15, "Asks to move to Viber"),
    "wechat": (18, "Asks to move to WeChat"),
    "google hangouts": (12, "Asks to move to Google Hangouts"),
    "text me": (10, "Requests to use text/SMS"),
    "private email": (18, "Requests private email communication"),

    # --- UNSOLICITED CONTACT & SPAMMY LANGUAGE ---
    "hi there": (5, "Generic greeting (potential mass message)"),
    "dear friend": (8, "Overly formal generic greeting"),
    "i found your": (12, "Claims to have found profile (unsolicited)"),
    "contact me directly": (12, "Pushes direct personal contact"),
    "check this link": (20, "Requests to click suspicious link"),
    "verify your account": (25, "Phishing attempt indicator"),
    "confirm your identity": (20, "Phishing indicator"),

    # --- PERSONAL INFORMATION REQUESTS (High Risk) ---
    "social security": (35, "Requests SSN"),
    "bank account": (35, "Requests bank account details"),
    "routing number": (35, "Requests banking information"),
    "credit card": (35, "Requests credit card information"),
    "passport": (30, "Requests passport/ID copy"),
    "driver license": (30, "Requests driver's license"),
    "home address": (25, "Requests home address"),
    "phone number": (15, "Early request for phone number"),
    "date of birth": (20, "Requests date of birth"),

    # --- JOB DESCRIPTION RED FLAGS ---
    "work from home": (10, "Generic work-from-home offer"),
    "no experience": (15, "Claims no experience required"),
    "unlimited earning": (20, "Promises unlimited earnings"),
    "get paid daily": (18, "Claims daily payment"),
    "easy money": (15, "Promises easy/quick money"),
    "part time": (8, "Part-time position (low indicator)"),
    "quick start": (12, "Pressure to start immediately"),
    "data entry": (10, "Generic data entry job"),
    "virtual assistant": (8, "Vague assistant role"),
    "customer service": (8, "Generic customer service"),

    # --- URGENCY & PRESSURE TACTICS ---
    "urgent": (10, "Creates urgency pressure"),
    "asap": (10, "Demands ASAP response"),
    "limited time": (12, "Time-limited opportunity"),
    "hurry": (10, "Rushing pressure tactic"),
    "act now": (10, "Pressure to act immediately"),
    "don't miss out": (12, "FOMO tactic"),
    "today only": (12, "Artificial deadline"),
    "spots available": (10, "Artificial scarcity"),

    # --- UNREALISTIC PROMISES ---
    "guaranteed": (15, "Uses guaranteed income language"),
    "risk free": (18, "Claims risk-free earnings"),
    "make $500": (12, "Unsubstantiated income claim (small)"),
    "make $1000": (15, "Unsubstantiated income claim (large)"),
    "make $5000": (20, "Unsubstantiated income claim (very large)"),
    "earn passive": (12, "Passive income promise"),
    "financial freedom": (10, "Vague freedom/wealth promise"),
    "life changing": (12, "Exaggerated opportunity claims"),
    "millionaire": (15, "Get rich quick indicator"),

    # --- VAGUE/EVASIVE LANGUAGE ---
    "it's complicated": (8, "Evasive explanation"),
    "i can't explain": (15, "Refuses to explain details"),
    "you'll understand later": (18, "Defers important details"),
    "just trust me": (20, "Requests blind trust"),
    "no questions asked": (15, "Discourages questions"),
    "don't ask": (18, "Explicitly avoids transparency"),

    # --- COMPANY/CREDENTIAL RED FLAGS ---
    "newly opened": (12, "Recently created company claim"),
    "secret company": (25, "Claims to be secret/exclusive"),
    "top secret": (25, "Suspicious secrecy claim"),
    "we are hiring": (5, "Generic recruitment (low indicator)"),
    "start your business": (10, "MLM/recruitment scheme indicator"),
    "be your own boss": (12, "MLM/entrepreneurship pitch"),
    "recruit others": (22, "Multi-level marketing indicator"),
    "referral bonus": (15, "MLM referral emphasis"),
    "hire you": (5, "Generic hiring language"),
    "hiring immediately": (8, "Suspicious immediate hiring claim"),

    # --- DUPLICATE/BATCH MESSAGE INDICATORS ---
    "copy and paste": (12, "Likely mass message"),
    "forwarding this": (10, "Forwarded mass message"),
    "bcc": (10, "Mass mailing indicator"),

    # --- ADDITIONAL PAYMENT METHODS ---
    "zelle": (18, "Requests Zelle transfer"),
    "moneypak": (28, "Mentions MoneyPak payment"),
    "google play": (28, "Requests Google Play card"),
    "steam card": (25, "Requests Steam gift card"),
    "walmart card": (25, "Requests Walmart gift card"),
    "target card": (25, "Requests Target gift card"),
    "square cash": (18, "Mentions Square Cash"),
    "venmo": (15, "Requests Venmo payment"),
    "stripe": (15, "Allows Stripe payment (context dependent)"),
    "ach transfer": (22, "Requests ACH bank transfer"),
    "check payment": (15, "Requests check/cheque"),
    "mobile wallet": (12, "Generic mobile wallet payment"),
    "nft": (20, "Involves NFT/blockchain transaction"),
    "wallet address": (25, "Requests cryptocurrency wallet address"),

    # --- MORE COMMUNICATION PLATFORMS ---
    "discord": (12, "Asks to move to Discord"),
    "slack": (12, "Asks to move to Slack"),
    "skype": (12, "Asks to move to Skype"),
    "messenger": (10, "Asks to move to Messenger"),
    "instagram": (12, "Asks to connect via Instagram"),
    "facebook": (10, "Asks to connect on Facebook"),
    "linkedin": (5, "Mentions LinkedIn (lower risk)"),
    "line app": (15, "Asks to move to LINE app"),
    "snapchat": (12, "Asks to communicate via Snapchat"),
    "tiktok": (12, "Asks to connect via TikTok"),
    "threema": (18, "Asks to use Threema"),

    # --- VISA/IMMIGRATION SCAMS ---
    "work visa": (20, "Promises to sponsor work visa"),
    "green card": (20, "Claims to help with green card"),
    "sponsorship": (18, "Offers employment sponsorship"),
    "immigration lawyer": (15, "Mentions immigration help"),
    "uk visa": (18, "UK work visa promise"),
    "au visa": (18, "Australian visa promise"),
    "canada visa": (18, "Canada visa promise"),

    # --- DOCUMENT & IDENTITY RED FLAGS ---
    "passport scan": (32, "Requests scanned passport"),
    "id photo": (30, "Requests ID photo"),
    "background check": (12, "Mentions background check fee"),
    "verification fee": (28, "Charges for verification"),
    "credit check": (18, "Requests credit check"),
    "document verification": (20, "Requests document verification"),
    "identity verification": (20, "Unclear identity verification"),
    "sign this contract": (8, "Rushed contract signing"),
    "non disclosure": (15, "NDA before job details"),
    "nda agreement": (15, "Suspicious NDA request"),

    # --- INTERVIEW & HIRING RED FLAGS ---
    "no interview": (18, "Hired without interview"),
    "phone interview": (5, "Phone interview mention (low risk)"),
    "skip the interview": (22, "Bypasses interview process"),
    "hire you today": (15, "Instant job offer"),
    "send your resume": (5, "Request for resume (low risk)"),
    "cover letter": (3, "Cover letter request (very low risk)"),
    "start tomorrow": (15, "Expects immediate start"),
    "we like you already": (12, "Premature job praise"),

    # --- MORE UNREALISTIC CLAIMS ---
    "doubles your money": (25, "Claims to double income"),
    "no experience needed": (14, "No qualifications required"),
    "zero experience": (15, "Zero experience OK"),
    "no skills": (15, "No skills needed claim"),
    "no training needed": (12, "No training required"),
    "work whenever": (10, "Flexible work claim"),
    "flexible hours": (5, "Flexible hours mention (low risk)"),
    "$100 per day": (14, "Specific unrealistic daily income"),
    "$200 per hour": (18, "Unrealistic hourly rate"),
    "100% commission": (20, "All commission-based work"),
    "no boss": (12, "No supervision claim"),
    "zero experience required": (16, "Zero qualifications needed"),

    # --- OVERLY FRIENDLY/LOVE SCAM TACTICS ---
    "sweetheart": (18, "Uses romantic language"),
    "my dear": (12, "Overly affectionate language"),
    "love you": (22, "Premature romantic language"),
    "beautiful person": (15, "Complimentary romantic language"),
    "soulmate": (20, "Romance scam indicator"),
    "miss you": (15, "Premature emotional language"),
    "special person": (12, "Excessive compliments"),
    "handsome": (10, "Complimentary attractiveness language"),

    # --- INCONSISTENCY & RED FLAGS ---
    "multiple jobs": (12, "Offers multiple simultaneous jobs"),
    "different company": (8, "Company name inconsistency"),
    "work for me": (10, "Direct personal employment"),
    "private company": (8, "Vague private company claims"),
    "offshore": (20, "Offshore employment mention"),
    "international": (8, "International work (context dependent)"),
    "remote position": (5, "Remote work mention (low risk)"),
    "freelance": (5, "Freelance work (low risk)"),

    # --- PHISHING/MALWARE INDICATORS ---
    "click here": (15, "Suspicious link request"),
    "download this": (20, "Requests suspicious download"),
    "install app": (18, "Requests to install app"),
    "enable javascript": (20, "Requests enabling JavaScript"),
    "allow notifications": (15, "Requests browser notifications"),
    "update your profile": (18, "Fake profile update request"),
    "complete your application": (12, "Vague application request"),

    # --- TAX & LEGAL RED FLAGS ---
    "tax deductible": (12, "Questionable tax claim"),
    "no taxes": (20, "Claims to avoid taxes"),
    "under the table": (25, "Cash/unreported work"),
    "off the books": (25, "Unreported employment claim"),
    "legal disclaimer": (10, "Vague legal disclaimer"),
    "not liable": (18, "Liability waiver language"),

    # --- ADULT CONTENT/INAPPROPRIATE ---
    "dating site": (18, "Dating/adult site relationship"),
    "adult chat": (25, "Adult chat service"),
    "cam girl": (25, "Adult cam work offer"),
    "escort": (25, "Escort service offer"),
    "sugar daddy": (22, "Sugar daddy arrangement"),

    # --- BLOCKCHAIN/CRYPTO RED FLAGS ---
    "smart contract": (20, "Blockchain contract mention"),
    "defi": (18, "DeFi platform involvement"),
    "yield farming": (22, "Yield farming scheme"),
    "staking": (15, "Cryptocurrency staking"),
    "launchpad": (18, "Token launchpad scheme"),
    "mining": (15, "Cryptocurrency mining claim"),
    "token airdrop": (20, "Free token airdrop"),

    # --- POOR ENGLISH/PROFESSIONALISM ---
    "grammer": (8, "Likely intentional misspelling"),
    "u r": (10, "Text speak language"),
    "4 u": (10, "Numerical text speak"),
    "thanx": (8, "Casual misspelling"),
    "yall": (5, "Casual southern dialect"),
    "aksed": (8, "Common misspelling (asked)"),

    # --- DUPLICATE/COPY-PASTE LANGUAGE ---
    "this message was sent": (10, "Mass message indicator"),
    "if interested": (8, "Generic follow-up language"),
    "feel free": (5, "Generic polite language"),
    "let me know": (3, "Generic closing language"),
    "best regards": (3, "Generic professional closing"),
    "yours truly": (4, "Formal generic closing"),

    # --- INCONSISTENT CONTACT INFO ---
    "gmail": (5, "Gmail used for business (context dependent)"),
    "yahoo": (5, "Yahoo email (outdated but low risk)"),
    "@gmail.com": (5, "Gmail business email (low risk)"),
    "no public email": (12, "Refuses public contact"),
    "private contact only": (15, "Only private contact allowed"),
    "use my personal": (12, "Directs to personal contact"),

    # --- TIMEFRAME RED FLAGS ---
    "just started": (10, "Recently created opportunity"),
    "brand new": (8, "New business/opportunity"),
    "opening soon": (8, "Opening announcement"),
    "closes soon": (12, "Artificial deadline"),
    "one time offer": (15, "Limited-time sole offer"),

    # --- GENERIC ROLE DESCRIPTIONS ---
    "manager": (3, "Generic manager role (very low risk)"),
    "coordinator": (3, "Coordinator role (very low risk)"),
    "analyst": (3, "Analyst role (very low risk)"),
    "specialist": (3, "Specialist role (very low risk)"),
    "consultant": (5, "Generic consultant role"),
    "advisor": (5, "Generic advisor role"),
    "representative": (5, "Generic representative role"),
}


def analyze_text(text: str) -> Tuple[int, str, List[str], List[str]]:
    """
    Analyze a recruiter message and return a risk assessment.

    Args:
        text: The recruiter message to analyze.

    Returns:
        A tuple of (score, level, flags, matched_phrases).
        - score: integer 0-100
        - level: "Low", "Medium", or "High"
        - flags: list of human-readable flag descriptions
        - matched_phrases: list of suspicious phrases found in the text
    """
    lower_text = text.lower()
    total_score = 0
    flags: List[str] = []
    matched_phrases: List[str] = []

    for phrase, (weight, description) in SUSPICIOUS_PATTERNS.items():
        if phrase in lower_text:
            total_score += weight
            flags.append(description)
            matched_phrases.append(phrase)

    # Clamp score to 0-100
    score = min(total_score, 100)

    # Determine risk level
    if score >= 60:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    return score, level, flags, matched_phrases
