import streamlit as st
import boto3
import snowflake.connector
import json
import configparser
import os
import toml
import pandas as pd
import time
from botocore.exceptions import ClientError

# Page configuration
st.set_page_config(
    page_title="Iceberg Table Creator",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("🧊 Iceberg Table Creator")
st.markdown("Automate the creation of Iceberg Tables on Snowflake with AWS S3 storage")

# Sidebar navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Choose a section:",
    ["🏗️ Infrastructure Setup", "🧊 Create Tables"],
    help="Switch between infrastructure setup and table creation"
)

# Show current status in sidebar
if st.session_state.get('infrastructure_ready'):
    st.sidebar.success("✅ Infrastructure Ready!")
    st.sidebar.info(f"External Volume: {st.session_state.get('external_volume_name', 'N/A')}")
    st.sidebar.info(f"S3 Bucket: {st.session_state.get('s3_bucket_name', 'N/A')}")
    if st.session_state.get('tables_created_count', 0) > 0:
        st.sidebar.info(f"Tables Created: {st.session_state.get('tables_created_count', 0)}")
else:
    st.sidebar.warning("⚠️ Infrastructure setup required")

# Reset button in sidebar
if st.sidebar.button("🔄 Reset All", help="Clear all data and start over"):
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")

# =============================================================================
# INFRASTRUCTURE SETUP PAGE
# =============================================================================
if page == "🏗️ Infrastructure Setup":
    st.header("🏗️ Infrastructure Setup")
    st.markdown("Set up AWS S3 bucket and Snowflake External Volume for Iceberg tables")
    
    # Connection file information
    st.subheader("📁 Connection Files")
    aws_creds_path = os.path.expanduser("~/.aws/credentials")
    sf_conn_path = os.path.expanduser("~/.snowflake/connections.toml")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📁 AWS Credentials: `{aws_creds_path}`")
    with col2:
        st.info(f"📁 Snowflake Config: `{sf_conn_path}`")
    
    # Setup instructions
    with st.expander("📚 Setup Instructions", expanded=False):
        st.markdown("""
        ### AWS Credentials Setup
        Create `~/.aws/credentials` with:
        ```
        [default]
        aws_access_key_id = your_access_key_id
        aws_secret_access_key = your_secret_access_key
        ```
        
        ### Snowflake Connection Setup
        Create `~/.snowflake/connections.toml` with:
        ```toml
        [connections.DEMO_PRAJAGOPAL_PUBLIC]
        account = "your_account"
        user = "your_username"
        password = "your_password"
        warehouse = "your_warehouse"
        database = "your_database"
        schema = "your_schema"
        ```
        """)
    
    st.markdown("---")
    
    # Infrastructure setup form
    with st.form("infrastructure_setup"):
        st.subheader("🔧 Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**AWS Configuration**")
            
            # AWS Regions dropdown
            aws_regions = [
                "us-east-1", "us-east-2", "us-west-1", "us-west-2",
                "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1", "eu-north-1",
                "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ap-northeast-2", "ap-south-1",
                "ca-central-1", "sa-east-1", "af-south-1", "me-south-1"
            ]
            aws_region = st.selectbox("AWS Region", aws_regions, index=3)  # Default to us-west-2
            
            s3_bucket_name = st.text_input("S3 Bucket Name", "sp500-top-10-sector-ohlcv-iceberg-s3bkt")
            iam_policy_name = st.text_input("IAM Policy Name", "snowflake-s3-top10-sp500-ohlcv-iceberg-iam-policy")
            iam_role_name = st.text_input("IAM Role Name", "snowflake-s3-top10-sp500-ohlcv-iceberg-iam-role")
        
        with col2:
            st.markdown("**Snowflake Configuration**")
            
            snowflake_external_volume_name = st.text_input("External Volume Name", "SP500_TOP10_SECTOR_OHLCV_ICEBERG_VOLUME")
            snowflake_connection_name = st.text_input("Connection Name", "DEMO_PRAJAGOPAL_PUBLIC")
            
            # Validate Snowflake connection
            sf_conn_path = os.path.expanduser("~/.snowflake/connections.toml")
            if os.path.exists(sf_conn_path):
                try:
                    sf_config = toml.load(sf_conn_path)
                    # Check both new format (connections.NAME) and old format (NAME)
                    connection_found = False
                    if f"connections.{snowflake_connection_name}" in sf_config:
                        connection_found = True
                    elif snowflake_connection_name in sf_config:
                        connection_found = True
                    
                    if connection_found:
                        st.success("✅ Snowflake connection found")
                    else:
                        available_connections = []
                        # Look for connections in both formats
                        for key in sf_config.keys():
                            if key.startswith("connections."):
                                available_connections.append(key.replace("connections.", ""))
                            elif isinstance(sf_config[key], dict) and 'account' in sf_config[key]:
                                available_connections.append(key)
                        
                        st.error(f"❌ Connection '{snowflake_connection_name}' not found")
                        if available_connections:
                            st.info(f"Available connections: {', '.join(available_connections)}")
                except Exception as e:
                    st.error(f"❌ Error reading connections: {e}")
            else:
                st.error("❌ Snowflake connections file not found")
        
        # Submit button
        setup_submitted = st.form_submit_button("🚀 Setup Infrastructure", type="primary")
    
    # Process infrastructure setup
    if setup_submitted:
        st.session_state.setup_submitted = True
        st.session_state.current_step = 0
        
        # Store configuration
        st.session_state.aws_region = aws_region
        st.session_state.s3_bucket_name = s3_bucket_name
        st.session_state.iam_policy_name = iam_policy_name
        st.session_state.iam_role_name = iam_role_name
        st.session_state.external_volume_name = snowflake_external_volume_name
        st.session_state.snowflake_connection_name = snowflake_connection_name

    # Show setup progress
    if st.session_state.get('setup_submitted'):
        st.markdown("---")
        st.header("⚙️ Setup Progress")
        
        # Progress tracking
        total_steps = 6
        current_step = st.session_state.get('current_step', 0)
        progress = st.progress(current_step / total_steps)
        
        # Load Snowflake connection parameters
        sf_conn_path = os.path.expanduser("~/.snowflake/connections.toml")
        try:
            sf_config = toml.load(sf_conn_path)
            # Try both new format (connections.NAME) and old format (NAME)
            sf_conn_params = None
            if f"connections.{st.session_state.snowflake_connection_name}" in sf_config:
                sf_conn_params = sf_config['connections'][st.session_state.snowflake_connection_name]
            elif st.session_state.snowflake_connection_name in sf_config:
                sf_conn_params = sf_config[st.session_state.snowflake_connection_name]
            
            if sf_conn_params is None:
                raise Exception(f"Connection '{st.session_state.snowflake_connection_name}' not found in either format")
                
        except Exception as e:
            st.error(f"❌ Failed to load Snowflake connection: {e}")
            st.stop()
        
        # Initialize AWS clients
        try:
            s3_client = boto3.client('s3', region_name=st.session_state.aws_region)
            iam_client = boto3.client('iam', region_name=st.session_state.aws_region)
        except Exception as e:
            st.error(f"❌ Failed to initialize AWS clients: {e}")
            st.stop()
        
        # Step 1: Create S3 Bucket
        if current_step == 0:
            with st.status("Step 1: Creating S3 Bucket...", expanded=True) as status:
                try:
                    st.write(f"🔍 Checking bucket: {st.session_state.s3_bucket_name}")
                    
                    # Check if bucket exists
                    bucket_exists = False
                    try:
                        s3_client.head_bucket(Bucket=st.session_state.s3_bucket_name)
                        st.write("✅ S3 bucket already exists")
                        bucket_exists = True
                    except ClientError as e:
                        if e.response['Error']['Code'] == '404':
                            st.write("📦 Creating new S3 bucket...")
                            # Create bucket
                            if st.session_state.aws_region == 'us-east-1':
                                s3_client.create_bucket(Bucket=st.session_state.s3_bucket_name)
                            else:
                                s3_client.create_bucket(
                                    Bucket=st.session_state.s3_bucket_name,
                                    CreateBucketConfiguration={'LocationConstraint': st.session_state.aws_region}
                                )
                            st.write("✅ S3 bucket created successfully")
                            bucket_exists = True
                        else:
                            raise e
                    
                    if bucket_exists:
                        st.session_state.current_step = 1
                        status.update(label="Step 1: S3 Bucket ✅", state="complete")
                        progress.progress(1 / total_steps)
                        time.sleep(0.5)  # Brief pause before next step
                        st.rerun()  # Trigger rerun to continue to next step
                        
                except Exception as e:
                    st.error(f"❌ S3 bucket creation failed: {e}")
                    st.write(f"Error details: {str(e)}")
                    st.stop()
        
        # Step 2: Create IAM Policy
        elif current_step == 1:
            with st.status("Step 2: Creating IAM Policy...", expanded=True) as status:
                try:
                    policy_document = {
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
                                "Resource": f"arn:aws:s3:::{st.session_state.s3_bucket_name}/*"
                            },
                            {
                                "Effect": "Allow",
                                "Action": [
                                    "s3:ListBucket",
                                    "s3:GetBucketLocation"
                                ],
                                "Resource": f"arn:aws:s3:::{st.session_state.s3_bucket_name}"
                            }
                        ]
                    }
                    
                    try:
                        response = iam_client.create_policy(
                            PolicyName=st.session_state.iam_policy_name,
                            PolicyDocument=json.dumps(policy_document)
                        )
                        policy_arn = response['Policy']['Arn']
                        st.write("✅ IAM policy created successfully")
                    except ClientError as e:
                        if e.response['Error']['Code'] == 'EntityAlreadyExists':
                            # Get existing policy ARN
                            account_id = boto3.client('sts').get_caller_identity()['Account']
                            policy_arn = f"arn:aws:iam::{account_id}:policy/{st.session_state.iam_policy_name}"
                            st.write("✅ IAM policy already exists")
                        else:
                            raise e
                    
                    st.session_state.policy_arn = policy_arn
                    st.session_state.current_step = 2
                    status.update(label="Step 2: IAM Policy ✅", state="complete")
                    progress.progress(2 / total_steps)
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ IAM policy creation failed: {e}")
                    st.stop()
        
        # Step 3: Create IAM Role
        elif current_step == 2:
            with st.status("Step 3: Creating IAM Role...", expanded=True) as status:
                try:
                    # Get current AWS account ID for initial trust policy
                    sts_client = boto3.client('sts', region_name=st.session_state.aws_region)
                    current_account_id = sts_client.get_caller_identity()['Account']
                    st.write(f"🔍 Using AWS Account ID: {current_account_id}")
                    
                    # Initial trust policy (will be updated later with Snowflake credentials)
                    initial_trust_policy = {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"AWS": f"arn:aws:iam::{current_account_id}:root"},
                                "Action": "sts:AssumeRole",
                                "Condition": {
                                    "StringEquals": {
                                        "sts:ExternalId": "temporary-placeholder"
                                    }
                                }
                            }
                        ]
                    }
                    
                    try:
                        response = iam_client.create_role(
                            RoleName=st.session_state.iam_role_name,
                            AssumeRolePolicyDocument=json.dumps(initial_trust_policy)
                        )
                        role_arn = response['Role']['Arn']
                        st.write("✅ IAM role created successfully")
                    except ClientError as e:
                        if e.response['Error']['Code'] == 'EntityAlreadyExists':
                            # Get existing role ARN
                            response = iam_client.get_role(RoleName=st.session_state.iam_role_name)
                            role_arn = response['Role']['Arn']
                            st.write("✅ IAM role already exists")
                        else:
                            raise e
                    
                    # Attach policy to role
                    iam_client.attach_role_policy(
                        RoleName=st.session_state.iam_role_name,
                        PolicyArn=st.session_state.policy_arn
                    )
                    
                    st.session_state.role_arn = role_arn
                    st.session_state.current_step = 3
                    status.update(label="Step 3: IAM Role ✅", state="complete")
                    progress.progress(3 / total_steps)
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ IAM role creation failed: {e}")
                    st.stop()
        
        # Step 4: Create Snowflake External Volume
        elif current_step == 3:
            with st.status("Step 4: Creating Snowflake External Volume...", expanded=True) as status:
                try:
                    conn = snowflake.connector.connect(**sf_conn_params)
                    cursor = conn.cursor()
                    
                    external_volume_sql = f"""
                    CREATE OR REPLACE EXTERNAL VOLUME {st.session_state.external_volume_name}
                    STORAGE_LOCATIONS = (
                        (
                            NAME = '{st.session_state.external_volume_name}'
                            STORAGE_PROVIDER = 'S3'
                            STORAGE_BASE_URL = 's3://{st.session_state.s3_bucket_name}/'
                            STORAGE_AWS_ROLE_ARN = '{st.session_state.role_arn}'
                        )
                    )
                    ALLOW_WRITES = TRUE;
                    """
                    
                    cursor.execute(external_volume_sql)
                    st.write("✅ External volume created successfully")
                    
                    conn.close()
                    st.session_state.current_step = 4
                    status.update(label="Step 4: External Volume ✅", state="complete")
                    progress.progress(4 / total_steps)
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ External volume creation failed: {e}")
                    st.stop()
        
        # Step 5: Get Snowflake credentials
        elif current_step == 4:
            with st.status("Step 5: Getting Snowflake Credentials...", expanded=True) as status:
                try:
                    conn = snowflake.connector.connect(**sf_conn_params)
                    cursor = conn.cursor()
                    
                    # Describe external volume
                    cursor.execute(f"DESC EXTERNAL VOLUME {st.session_state.external_volume_name}")
                    desc_results = cursor.fetchall()
                    
                    # Parse results
                    storage_location_prop_value = None
                    for row in desc_results:
                        if len(row) > 1 and row[1] == 'STORAGE_LOCATION_1':
                            storage_location_prop_value = row[3]
                            break
                    
                    if storage_location_prop_value:
                        location_data = json.loads(storage_location_prop_value)
                        iam_user_arn = location_data.get("STORAGE_AWS_IAM_USER_ARN")
                        external_id = location_data.get("STORAGE_AWS_EXTERNAL_ID")
                        
                        st.write(f"✅ IAM User ARN: {iam_user_arn}")
                        st.write(f"✅ External ID: {external_id}")
                        
                        st.session_state.iam_user_arn = iam_user_arn
                        st.session_state.external_id = external_id
                    else:
                        raise Exception("Could not find STORAGE_LOCATION_1 in external volume description")
                    
                    conn.close()
                    st.session_state.current_step = 5
                    status.update(label="Step 5: Snowflake Credentials ✅", state="complete")
                    progress.progress(5 / total_steps)
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Getting Snowflake credentials failed: {e}")
                    st.stop()
        
        # Step 6: Update IAM Role Trust Policy
        elif current_step == 5:
            with st.status("Step 6: Updating IAM Role Trust Policy...", expanded=True) as status:
                try:
                    # Update trust policy with Snowflake credentials
                    updated_trust_policy = {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"AWS": st.session_state.iam_user_arn},
                                "Action": "sts:AssumeRole",
                                "Condition": {
                                    "StringEquals": {
                                        "sts:ExternalId": st.session_state.external_id
                                    }
                                }
                            }
                        ]
                    }
                    
                    iam_client.update_assume_role_policy(
                        RoleName=st.session_state.iam_role_name,
                        PolicyDocument=json.dumps(updated_trust_policy)
                    )
                    
                    st.write("✅ IAM role trust policy updated successfully")
                    
                    st.session_state.current_step = 6
                    st.session_state.infrastructure_ready = True
                    st.session_state.sf_conn_params = sf_conn_params
                    status.update(label="Step 6: Trust Policy ✅", state="complete")
                    progress.progress(6 / total_steps)
                    time.sleep(1.0)  # Longer pause before showing completion
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Trust policy update failed: {e}")
                    st.stop()
        
        # Setup complete
        if st.session_state.get('infrastructure_ready'):
            st.success("🎉 Infrastructure setup complete!")
            st.balloons()
            
            # Show configuration summary
            with st.expander("📋 Configuration Summary", expanded=False):
                st.write(f"**AWS Region:** {st.session_state.aws_region}")
                st.write(f"**S3 Bucket:** {st.session_state.s3_bucket_name}")
                st.write(f"**IAM Policy:** {st.session_state.iam_policy_name}")
                st.write(f"**IAM Role:** {st.session_state.iam_role_name}")
                st.write(f"**External Volume:** {st.session_state.external_volume_name}")
            
            st.info("👈 Now switch to 'Create Tables' in the sidebar to start creating Iceberg tables!")

# =============================================================================
# CREATE TABLES PAGE
# =============================================================================
elif page == "🧊 Create Tables":
    st.header("🧊 Create Iceberg Tables")
    
    # Check if infrastructure is ready
    if not st.session_state.get('infrastructure_ready'):
        st.warning("⚠️ Infrastructure setup required first!")
        st.info("👈 Please complete the 'Infrastructure Setup' first in the sidebar.")
        st.stop()
    
    st.success("✅ Using existing infrastructure setup")
    
    # Show current infrastructure info
    with st.expander("📋 Current Infrastructure", expanded=False):
        st.write(f"**External Volume:** {st.session_state.get('external_volume_name')}")
        st.write(f"**S3 Bucket:** {st.session_state.get('s3_bucket_name')}")
        st.write(f"**AWS Region:** {st.session_state.get('aws_region')}")
    
    st.markdown("---")
    
    # Table creation form
    with st.form("table_creation"):
        st.subheader("🛠️ Table Configuration")
        
        # Get available databases and schemas
        available_databases = ['DEMODB']  # Default fallback
        available_schemas = ['PUBLIC']    # Default fallback
        
        try:
            if st.session_state.get('sf_conn_params'):
                conn = snowflake.connector.connect(**st.session_state.sf_conn_params)
                cursor = conn.cursor()
                
                # Get databases
                cursor.execute("SHOW DATABASES")
                db_results = cursor.fetchall()
                available_databases = [row[1] for row in db_results]
                
                # Get schemas for default database
                if available_databases:
                    cursor.execute(f"SHOW SCHEMAS IN DATABASE {available_databases[0]}")
                    schema_results = cursor.fetchall()
                    available_schemas = [row[1] for row in schema_results]
                
                conn.close()
        except Exception as e:
            st.warning(f"Could not fetch databases/schemas: {e}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Database & Schema**")
            selected_database = st.selectbox("Database", available_databases, key="db_select")
            selected_schema = st.selectbox("Schema", available_schemas, key="schema_select")
            
            table_name = st.text_input(
                "Table Name *", 
                placeholder="e.g., my_stock_data_table",
                help="Enter a unique name for your Iceberg table",
                key="table_name"
            )
        
        with col2:
            st.markdown("**Quick Templates**")
            template_choice = st.selectbox(
                "Choose a template (optional)",
                ["Custom", "Stock Data", "User Data", "Sales Data"],
                help="Select a template to auto-populate columns"
            )
            
            if template_choice != "Custom":
                st.info(f"✅ {template_choice} template will be applied")
        
        # Column definitions
        st.markdown("**Column Definitions**")
        
        # Apply template if selected
        template_columns = []
        if template_choice == "Stock Data":
            template_columns = [
                {"name": "TICKER", "type": "VARCHAR"},
                {"name": "TRADE_DATE", "type": "DATE"},
                {"name": "OPEN_PRICE", "type": "DOUBLE"},
                {"name": "HIGH_PRICE", "type": "DOUBLE"},
                {"name": "LOW_PRICE", "type": "DOUBLE"},
                {"name": "CLOSE_PRICE", "type": "DOUBLE"},
                {"name": "VOLUME", "type": "BIGINT"}
            ]
        elif template_choice == "User Data":
            template_columns = [
                {"name": "USER_ID", "type": "INTEGER"},
                {"name": "USERNAME", "type": "VARCHAR"},
                {"name": "EMAIL", "type": "VARCHAR"},
                {"name": "CREATED_DATE", "type": "TIMESTAMP"},
                {"name": "IS_ACTIVE", "type": "BOOLEAN"}
            ]
        elif template_choice == "Sales Data":
            template_columns = [
                {"name": "ORDER_ID", "type": "INTEGER"},
                {"name": "CUSTOMER_ID", "type": "INTEGER"},
                {"name": "PRODUCT_NAME", "type": "VARCHAR"},
                {"name": "QUANTITY", "type": "INTEGER"},
                {"name": "PRICE", "type": "DECIMAL"},
                {"name": "ORDER_DATE", "type": "DATE"}
            ]
        
        # Show template columns or allow custom input
        if template_choice != "Custom" and template_columns:
            st.write("**Template Columns:**")
            for i, col in enumerate(template_columns):
                st.write(f"{i+1}. **{col['name']}** ({col['type']})")
            columns_to_use = template_columns
        else:
            st.write("**Custom Columns:**")
            
            # Custom column input interface
            data_types = [
                "VARCHAR", "STRING", "TEXT",
                "INTEGER", "BIGINT", "SMALLINT", "TINYINT",
                "DECIMAL", "NUMERIC", "DOUBLE", "FLOAT", "REAL",
                "BOOLEAN",
                "DATE", "TIME", "DATETIME", "TIMESTAMP", "TIMESTAMP_LTZ", "TIMESTAMP_NTZ", "TIMESTAMP_TZ",
                "BINARY", "VARBINARY",
                "VARIANT", "OBJECT", "ARRAY"
            ]
            
            # Allow adding multiple columns within the form
            num_columns = st.number_input("Number of columns", min_value=1, max_value=20, value=3)
            
            custom_columns = []
            for i in range(num_columns):
                col1, col2 = st.columns(2)
                with col1:
                    col_name = st.text_input(f"Column {i+1} Name", key=f"col_name_{i}", placeholder="e.g., CUSTOMER_ID")
                with col2:
                    col_type = st.selectbox(f"Column {i+1} Type", data_types, key=f"col_type_{i}")
                
                if col_name:  # Only add if name is provided
                    custom_columns.append({"name": col_name.upper().strip(), "type": col_type})
            
            columns_to_use = custom_columns
        
        # Submit button
        create_submitted = st.form_submit_button("🚀 Create Iceberg Table", type="primary")
    
    # Process table creation
    if create_submitted:
        # Validation
        validation_errors = []
        
        if not table_name:
            validation_errors.append("Please enter a table name")
        
        if not columns_to_use:
            validation_errors.append("Please select a template or define at least one custom column")
        
        # Validate table name
        import re
        if table_name and not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table_name):
            validation_errors.append("Table name must start with letter/underscore and contain only letters, numbers, underscores")
        
        # Validate column names
        for i, col in enumerate(columns_to_use):
            if not col.get('name'):
                validation_errors.append(f"Column {i+1} name is required")
            elif not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col['name']):
                validation_errors.append(f"Column '{col['name']}' must start with letter/underscore and contain only letters, numbers, underscores")
        
        if validation_errors:
            st.error("❌ Please fix the following issues:")
            for error in validation_errors:
                st.write(f"  • {error}")
        else:
            # Store table creation info
            st.session_state.table_to_create = {
                'database': selected_database,
                'schema': selected_schema,
                'table_name': table_name,
                'columns': columns_to_use,
                'full_name': f"{selected_database}.{selected_schema}.{table_name}",
                'base_location': f"{selected_database.lower()}.{selected_schema.lower()}.{table_name.lower()}"
            }
            st.session_state.create_table_now = True

    # Execute table creation
    if st.session_state.get('create_table_now'):
        table_info = st.session_state.table_to_create
        
        st.markdown("---")
        st.header("🧊 Creating Table")
        
        try:
            # Connect to Snowflake
            conn = snowflake.connector.connect(**st.session_state.sf_conn_params)
            cursor = conn.cursor()
            
            # Set context
            cursor.execute(f"USE DATABASE {table_info['database']}")
            cursor.execute(f"USE SCHEMA {table_info['schema']}")
            
            # Generate CREATE TABLE SQL
            columns_sql = ",\n    ".join([f"{col['name']} {col['type']}" for col in table_info['columns']])
            
            create_sql = f"""CREATE OR REPLACE ICEBERG TABLE {table_info['table_name']}
(
    {columns_sql}
)
CATALOG = 'SNOWFLAKE'
EXTERNAL_VOLUME = '{st.session_state.external_volume_name}'
BASE_LOCATION = '{table_info['base_location']}';"""
            
            # Execute table creation
            with st.status("Creating Iceberg table...", expanded=True) as status:
                st.code(create_sql, language='sql')
                cursor.execute(create_sql)
                st.write("✅ Table created successfully!")
                status.update(label="Table Creation ✅", state="complete")
            
            # Insert sample data
            with st.status("Inserting sample data...", expanded=True) as status:
                sample_data = []
                for i in range(5):
                    row = []
                    for col in table_info['columns']:
                        if col['type'] in ['VARCHAR', 'STRING', 'TEXT']:
                            row.append(f"'Sample_{i+1}'")
                        elif col['type'] in ['INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT']:
                            row.append(str(100 + i))
                        elif col['type'] in ['DOUBLE', 'FLOAT', 'REAL', 'DECIMAL', 'NUMERIC']:
                            row.append(str(100.50 + i))
                        elif col['type'] == 'BOOLEAN':
                            row.append('TRUE' if i % 2 == 0 else 'FALSE')
                        elif col['type'] in ['DATE', 'DATETIME', 'TIMESTAMP', 'TIMESTAMP_LTZ', 'TIMESTAMP_NTZ', 'TIMESTAMP_TZ']:
                            row.append(f"'2024-01-{15 + i:02d}'")
                        else:
                            row.append("'default_value'")
                    sample_data.append(f"({', '.join(row)})")
                
                insert_sql = f"INSERT INTO {table_info['table_name']} VALUES {', '.join(sample_data)}"
                cursor.execute(insert_sql)
                st.write("✅ Sample data inserted!")
                status.update(label="Data Insertion ✅", state="complete")
            
            # Query and display results
            with st.status("Querying results...", expanded=True) as status:
                cursor.execute(f"SELECT COUNT(*) FROM {table_info['table_name']}")
                count_result = cursor.fetchone()
                st.write(f"✅ Row count: {count_result[0]}")
                
                cursor.execute(f"SELECT * FROM {table_info['table_name']} LIMIT 10")
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                
                df = pd.DataFrame(results, columns=column_names)
                st.dataframe(df)
                status.update(label="Query Results ✅", state="complete")
            
            # Verify S3 files
            with st.status("Verifying S3 files...", expanded=True) as status:
                s3_client = boto3.client('s3', region_name=st.session_state.aws_region)
                response = s3_client.list_objects_v2(
                    Bucket=st.session_state.s3_bucket_name,
                    Prefix=table_info['base_location']
                )
                
                if 'Contents' in response:
                    st.write(f"✅ Found {len(response['Contents'])} files in S3:")
                    for obj in response['Contents'][:10]:  # Show first 10 files
                        st.write(f"  • {obj['Key']} ({obj['Size']} bytes)")
                else:
                    st.write("⚠️ No files found in S3 yet (may take a moment)")
                
                status.update(label="S3 Verification ✅", state="complete")
            
            conn.close()
            
            # Track created table
            if 'created_tables' not in st.session_state:
                st.session_state.created_tables = []
            
            st.session_state.created_tables.append({
                'name': table_info['full_name'],
                'base_location': table_info['base_location'],
                'columns': table_info['columns'],
                'created_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            st.session_state.tables_created_count = len(st.session_state.created_tables)
            
            # Success message
            st.success(f"🎉 Table '{table_info['full_name']}' created successfully!")
            
            # Clear creation state
            del st.session_state.create_table_now
            del st.session_state.table_to_create
            
            if st.button("➕ Create Another Table", type="primary"):
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Table creation failed: {e}")
    
    # Show created tables
    if st.session_state.get('created_tables'):
        st.markdown("---")
        st.subheader("📊 Created Tables")
        
        for i, table in enumerate(st.session_state.created_tables):
            with st.expander(f"Table {i+1}: {table['name']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Created:** {table['created_at']}")
                    st.write(f"**S3 Location:** s3://{st.session_state.s3_bucket_name}/{table['base_location']}/")
                with col2:
                    st.write("**Schema:**")
                    for col in table['columns']:
                        st.write(f"  • {col['name']} ({col['type']})")

st.markdown("---")
st.markdown("*Iceberg Table Creator - Automated AWS S3 + Snowflake Setup*")