# 🤖 AI-Assisted Development Guide

**Recreate the Iceberg Table Creator using Cursor or any AI coding assistant**

This document contains the exact prompts and instructions used to build this Streamlit application. Follow these prompts sequentially with your AI assistant to recreate the entire project from scratch.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.8+ installed
- Cursor IDE or similar AI coding assistant
- Basic understanding of Streamlit, AWS, and Snowflake concepts
- AWS account with programmatic access
- Snowflake account

## 🎯 Development Approach

This project was built using **iterative AI-assisted development** with the following principles:
- Start with core functionality, then enhance
- Test frequently and fix issues immediately
- Use AI for both code generation and problem-solving
- Maintain clean, readable code structure

---

## 🚀 Phase 1: Initial Project Setup

### **Prompt 1.1: Project Initialization**
```
I want to create a Streamlit application to automate the creation of Iceberg Tables on Snowflake. This automation involves a multi-step process:

1. Creating an AWS S3 bucket
2. Creating a specific AWS IAM Policy for the S3 bucket
3. Creating an AWS IAM Role with an initial placeholder trust policy
4. Creating a Snowflake External Volume linked to the S3 bucket and IAM role
5. Describing the Snowflake External Volume to extract the STORAGE_AWS_IAM_USER_ARN and STORAGE_AWS_EXTERNAL_ID
6. Updating the AWS IAM Role's trust policy with the extracted Snowflake credentials

The app should display all configuration data (S3 bucket name, IAM Policy, IAM Role, Snowflake External Volume details) and use pre-defined AWS credentials (~/.aws/credentials) and Snowflake connection details (~/.snowflake/connections.toml, connection name DEMO_PRAJAGOPAL_PUBLIC).

Create the basic Streamlit app structure with the required imports and page configuration.
```

### **Prompt 1.2: Core Infrastructure Setup**
```
Now implement the core infrastructure automation logic. The app should:

1. Create a form to collect user inputs:
   - AWS region (dropdown with major regions)
   - S3 bucket name
   - IAM policy name  
   - IAM role name
   - Snowflake external volume name
   - Snowflake connection name

2. Show the connection file paths and setup instructions for:
   - AWS credentials file (~/.aws/credentials)
   - Snowflake connections file (~/.snowflake/connections.toml)

3. Implement the 6-step automation process with progress tracking:
   - Step 1: Create S3 bucket (handle existing buckets)
   - Step 2: Create IAM policy with S3 permissions
   - Step 3: Create IAM role with initial trust policy
   - Step 4: Create Snowflake External Volume
   - Step 5: Parse DESC EXTERNAL VOLUME output to extract Snowflake credentials
   - Step 6: Update IAM role trust policy with Snowflake credentials

Include proper error handling and status updates for each step.
```

### **Prompt 1.3: Connection Management**
```
The app is failing to find the Snowflake connections.toml file. The file exists but uses the old TOML format:

[DEMO_PRAJAGOPAL_PUBLIC]
account = "IHB90733"
user = "prajagopal"
# ... other settings

But the app expects the new format with connections.NAME. Fix the connection loading logic to handle both old format (NAME) and new format (connections.NAME) automatically. Also improve error messages to show available connections if the specified one is not found.
```

---

## 🧊 Phase 2: Table Creation Interface

### **Prompt 2.1: Basic Table Creation**
```
Now add Iceberg table creation functionality. The app should have a second section that:

1. Only appears after infrastructure setup is complete
2. Allows users to create Iceberg tables using the configured external volume
3. Provides input fields for:
   - Database name (dropdown populated from Snowflake)
   - Schema name (dropdown populated from Snowflake)  
   - Table name (text input with validation)
   - Column definitions with name and data type

4. Include these built-in templates:
   - Stock Data: TICKER, TRADE_DATE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, VOLUME
   - User Data: USER_ID, USERNAME, EMAIL, CREATED_DATE, IS_ACTIVE
   - Sales Data: ORDER_ID, CUSTOMER_ID, PRODUCT_NAME, QUANTITY, PRICE, ORDER_DATE

5. After table creation, automatically:
   - Insert sample test data based on column types
   - Query the table to verify data
   - Check S3 bucket for created Iceberg files
   - Display results in a user-friendly format

Include proper SQL name validation and error handling.
```

### **Prompt 2.2: Enhanced Column Management**
```
The current table creation has issues with premature execution and form conflicts. Fix these problems:

1. Table creation should ONLY happen when the user explicitly clicks "Create Iceberg Table" button
2. Users should be able to add multiple columns without triggering table creation
3. Add real-time SQL name validation for table and column names
4. Include a comprehensive list of Snowflake data types (23+ types)
5. Show validation status and enable/disable the create button based on validation
6. Add the ability to create multiple tables using the same infrastructure setup

The app should have a clean, logical flow: enter table name → add columns → validate → create (only when button clicked).
```

### **Prompt 2.3: Fix Form Button Conflicts**
```
The app is showing "StreamlitAPIException: st.button() can't be used in an st.form()" errors. Fix this by:

1. Moving all interactive buttons outside of form contexts
2. Using separate click tracking variables instead of inline button logic
3. Ensuring template buttons, add/delete column buttons, and other interactive elements work without form conflicts
4. Maintaining the same functionality but with proper Streamlit form structure

The table creation should be completely controlled - no automatic execution when inputs change.
```

---

## 🏗️ Phase 3: Architecture Redesign

### **Prompt 3.1: Two-Form Architecture**
```
The current single-form approach is causing state management issues and complexity. Redesign the app with a clean two-form structure:

1. **Sidebar Navigation** with two main sections:
   - "Infrastructure Setup" - S3 bucket and External Volume configuration  
   - "Create Tables" - Iceberg table creation using existing setup

2. **Infrastructure Setup Form**:
   - Single purpose: AWS S3 + Snowflake External Volume setup
   - Clean progress tracking with visual indicators
   - One-time setup that persists across page switches

3. **Table Creation Form**:
   - Dedicated page for creating tables
   - Template support and custom column definitions
   - Reuses existing infrastructure without repetition

4. **State Management**:
   - Infrastructure setup state persists when switching between forms
   - Clean separation of concerns
   - Table tracking across sessions

This should eliminate form conflicts and provide a much cleaner user experience.
```

### **Prompt 3.2: Progress Step Issues**
```
The app is getting stuck at infrastructure setup steps. The progress steps are using >= logic which means multiple steps try to run simultaneously. Fix this by:

1. Changing step logic from "if current_step >= N" to "elif current_step == N"
2. Adding explicit step progression with st.rerun() after each completion
3. Including small delays between steps for better UX
4. Adding more detailed logging for each step
5. Using exact step matching to ensure only one step runs at a time

The setup should flow smoothly: Step 0 → Step 1 → Step 2 → ... → Step 6 → Completion
```

### **Prompt 3.3: IAM Role Trust Policy Fix**
```
The IAM role creation is failing with "Invalid principal in policy" error because it's using a fake AWS account ID (123456789012). Fix this by:

1. Getting the current AWS account ID dynamically using STS
2. Using the real account ID in the initial trust policy
3. Adding debug information to show which account ID is being used
4. Ensuring the trust policy is valid before role creation

The initial trust policy should use the actual AWS account ID, then get updated later with Snowflake credentials.
```

---

## 🎨 Phase 4: User Experience Enhancement

### **Prompt 4.1: Custom Column Input Interface**
```
The table creation form shows "Add your custom columns after submitting this form" but provides no way to actually add columns when "Custom" is selected. Fix this by:

1. Adding a proper column management interface within the form when "Custom" is selected
2. Allow users to specify number of columns (1-20)
3. Provide column name inputs and data type dropdowns for each column
4. Include comprehensive Snowflake data types (VARCHAR, INTEGER, DOUBLE, BOOLEAN, DATE, TIMESTAMP, etc.)
5. Show real-time validation for column names
6. Only include columns that have names provided

The form should work seamlessly for both templates and custom column definitions.
```

### **Prompt 4.2: Final Polish and Validation**
```
Add final polish to the app:

1. **Comprehensive Validation**:
   - SQL name validation with regex checking
   - Reserved word detection
   - Real-time feedback with green checkmarks and red errors
   - Progressive validation messages

2. **Enhanced User Experience**:
   - Clear status messages throughout the process
   - Professional error handling with helpful solutions
   - Table creation tracking and history
   - Ability to create multiple tables without repeating infrastructure setup

3. **Testing and Verification**:
   - Automatic sample data insertion based on column types
   - Query result display with pandas DataFrames
   - S3 file verification and listing
   - Complete end-to-end testing workflow

The app should feel professional and provide clear feedback at every step.
```

---

## 📦 Phase 5: Production Package Creation

### **Prompt 5.1: GitHub Repository Setup**
```
Create a complete GitHub-ready package for this Streamlit app that makes installation and deployment absolutely joyful for users. The target experience should be:

1. Clone → One command
2. Install → One command (automated environment setup)  
3. Configure → Copy-paste templates provided
4. Run → One command
5. Create Tables → Pure joy!

Create these files:
- Professional README.md with badges, clear instructions, and examples
- install.sh script for one-command setup
- requirements.txt with all dependencies
- .gitignore for Python projects
- LICENSE file (MIT)
- run.sh script for easy launching

The documentation should be so good that users feel excited to try the app rather than intimidated by setup complexity.
```

### **Prompt 5.2: Comprehensive Documentation**
```
Create additional documentation files to make this a world-class open source project:

1. **TROUBLESHOOTING.md**: Common issues and solutions covering:
   - Installation problems (Python, permissions, dependencies)
   - Connection issues (AWS credentials, Snowflake connections)
   - S3 and IAM problems with specific error messages and fixes
   - Network and Streamlit issues

2. **EXAMPLES.md**: Real-world usage examples for different industries:
   - Financial data pipelines (stock market data)
   - User management systems (SaaS applications)  
   - E-commerce analytics (orders and inventory)
   - IoT sensor data collection
   - Healthcare data management
   - Marketing campaign analytics

3. **DEPLOYMENT.md**: Multiple deployment options:
   - Local development setup
   - Docker deployment with docker-compose
   - Cloud deployment (AWS ECS, Google Cloud Run, Azure)
   - Streamlit Cloud deployment
   - Security considerations and best practices

Include code examples, configuration templates, and step-by-step instructions for each scenario.
```

### **Prompt 5.3: Docker and CI/CD Setup**
```
Add production-ready deployment capabilities:

1. **Docker Setup**:
   - Dockerfile for containerized deployment
   - docker-compose.yml for easy local deployment
   - Health checks and proper port configuration
   - Volume mounts for credentials

2. **GitHub Actions**:
   - Automated testing on multiple Python versions (3.8-3.11)
   - Security scanning with bandit and safety
   - Code quality checks with flake8
   - Documentation validation
   - Markdown link checking

3. **Additional Files**:
   - .github/workflows/test.yml for CI pipeline
   - Enhanced .gitignore for all deployment scenarios
   - Project structure documentation

The goal is to make this a professional, production-ready project that can be deployed anywhere.
```

---

## 📋 Required IAM Configurations

### **Sample IAM Policy JSON**
The IAM policy that gets created for S3 bucket access should follow this structure:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject", 
                "s3:GetObjectVersion",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion"
            ],
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME",
            "Condition": {
                "StringLike": {
                    "s3:prefix": ["*"]
                }
            }
        }
    ]
}
```

### **Sample IAM Role Trusted Relationship JSON**
The IAM role trust policy gets updated with Snowflake credentials and should follow this structure:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::123456789012:user/snowflake-user"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "ACCOUNT123_SFCRole=1_ExampleExternalId12345="
                }
            }
        }
    ]
}
```

**Important Notes:**
- The `Principal.AWS` value comes from Snowflake's `STORAGE_AWS_IAM_USER_ARN`
- The `sts:ExternalId` value comes from Snowflake's `STORAGE_AWS_EXTERNAL_ID`
- These values are automatically extracted from the `DESC EXTERNAL VOLUME` command
- The app handles the initial trust policy creation with a placeholder and updates it automatically

---

## 🎯 Key Development Principles Used

### **1. Iterative Development**
- Start with MVP, then enhance progressively
- Test each feature before moving to the next
- Fix issues immediately when they arise

### **2. User-Centric Design**
- Focus on user experience over technical complexity
- Provide clear feedback and error messages
- Make the "happy path" as smooth as possible

### **3. Professional Standards**
- Comprehensive documentation
- Multiple deployment options
- Security best practices
- Community-friendly licensing and contributing guidelines

### **4. AI-Assisted Problem Solving**
- Use AI for both code generation and debugging
- Iterate on solutions based on testing feedback
- Leverage AI for documentation and examples

---

## 🔧 Technical Architecture Decisions

### **State Management**
- Use Streamlit session_state for persistence
- Separate infrastructure and table creation state
- Clean state transitions between app sections

### **Error Handling**
- Graceful degradation for missing credentials
- Clear error messages with actionable solutions
- Comprehensive validation at multiple levels

### **Security**
- Never commit credentials to version control
- Support multiple credential management approaches
- Provide security guidance in documentation

### **Deployment Flexibility**
- Support local, Docker, and cloud deployment
- Environment variable configuration
- Health checks and monitoring capabilities

---

## 📚 Learning Outcomes

Building this project teaches:

1. **Streamlit Development**: Advanced Streamlit patterns and best practices
2. **AWS Integration**: S3, IAM, and STS service integration
3. **Snowflake Operations**: External volumes and Iceberg table management
4. **DevOps Practices**: Docker, CI/CD, and deployment automation
5. **Documentation**: Creating user-friendly, comprehensive documentation
6. **Open Source**: Professional project structure and community engagement

---

## 🚀 Usage Instructions

To use these prompts:

1. **Start with Phase 1** and work sequentially
2. **Test frequently** after each prompt
3. **Adapt prompts** based on your specific requirements
4. **Iterate and improve** based on testing feedback
5. **Add your own enhancements** once core functionality works

### **Tips for Success**
- Copy prompts exactly as written for best results
- Test each phase before moving to the next
- Use the troubleshooting guide when issues arise
- Customize the final product for your specific use case

---

**Happy coding!** 🎉 These prompts will help you recreate this entire project and understand the development process that created it.

---

*This prompt guide was created alongside the actual development of the Iceberg Table Creator, capturing the real prompts and iterative process used to build the application.*
