# 🔧 Troubleshooting Guide

Common issues and their solutions for the Iceberg Table Creator.

## 🚨 Installation Issues

### **"Python 3 is not installed"**
**Solution:**
- **macOS**: `brew install python3` or download from [python.org](https://python.org)
- **Ubuntu**: `sudo apt update && sudo apt install python3 python3-pip`
- **Windows**: Download from [python.org](https://python.org) and add to PATH

### **"Permission denied: ./install.sh"**
**Solution:**
```bash
chmod +x install.sh
./install.sh
```

### **"Virtual environment creation failed"**
**Solution:**
```bash
# Install venv if missing
sudo apt install python3-venv  # Ubuntu
# or
pip3 install virtualenv  # Alternative
```

## 🔐 Connection Issues

### **"Connection 'DEMO_PRAJAGOPAL_PUBLIC' not found"**
**Problem:** Snowflake connection file format or name mismatch

**Solution:**
1. Check file exists: `ls -la ~/.snowflake/connections.toml`
2. Verify format:
```toml
[DEMO_PRAJAGOPAL_PUBLIC]
account = "YOUR_ACCOUNT"
user = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
database = "YOUR_DATABASE"
schema = "YOUR_SCHEMA"
```
3. Match connection name exactly in the app

### **"AWS credentials not configured"**
**Problem:** Missing or incorrect AWS credentials

**Solution:**
1. Create credentials file:
```bash
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
EOF
```
2. Test with: `aws sts get-caller-identity`

### **"Invalid principal in policy"**
**Problem:** IAM trust policy has invalid AWS account reference

**Solution:** This should be auto-fixed in the latest version. If it persists:
1. Check your AWS credentials are valid
2. Ensure your IAM user has `sts:GetCallerIdentity` permission

## 🪣 S3 Issues

### **"S3 bucket creation failed: BucketAlreadyExists"**
**Problem:** Bucket name is globally taken

**Solution:**
- Try a more unique bucket name
- Add timestamp: `my-iceberg-bucket-20241219`
- Add random suffix: `my-iceberg-bucket-xyz123`

### **"Access Denied" on S3 operations**
**Problem:** Insufficient S3 permissions

**Solution:**
Attach this policy to your AWS user:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::*",
                "arn:aws:s3:::*/*"
            ]
        }
    ]
}
```

## 👤 IAM Issues

### **"User is not authorized to perform: iam:CreateRole"**
**Problem:** Insufficient IAM permissions

**Solution:**
Your AWS user needs these policies:
- `IAMFullAccess` (or custom policy with `iam:*` permissions)
- `STSAssumeRoleAccess`

### **"Role already exists"**
**Problem:** IAM role name conflict

**Solution:**
- The app handles this automatically (uses existing role)
- If issues persist, use a different role name

## ❄️ Snowflake Issues

### **"Invalid account identifier"**
**Problem:** Wrong Snowflake account format

**Solution:**
Use the full account identifier:
- **Format**: `ACCOUNT.REGION.PROVIDER`
- **Example**: `ABC12345.us-west-2.aws`
- **Find it**: Snowflake UI → Admin → Accounts

### **"Insufficient privileges to create external volume"**
**Problem:** User lacks required Snowflake permissions

**Solution:**
Your Snowflake user needs:
- `ACCOUNTADMIN` role, or
- Custom role with these privileges:
  - `CREATE EXTERNAL VOLUME`
  - `CREATE DATABASE`
  - `CREATE SCHEMA`
  - `CREATE TABLE`

### **"External volume creation failed"**
**Problem:** Various Snowflake configuration issues

**Solution:**
1. Check your Snowflake connection works:
```python
import snowflake.connector
conn = snowflake.connector.connect(
    account='YOUR_ACCOUNT',
    user='YOUR_USER',
    password='YOUR_PASSWORD'
)
```
2. Verify your IAM role ARN is correct
3. Ensure S3 bucket exists and is accessible

## 🧊 Table Creation Issues

### **"Table creation failed: SQL compilation error"**
**Problem:** Invalid SQL syntax in table definition

**Solution:**
- Check column names use only letters, numbers, underscores
- Ensure column names don't start with numbers
- Avoid SQL reserved words (SELECT, FROM, etc.)

### **"No files found in S3"**
**Problem:** Iceberg files not appearing in S3

**Solution:**
- Wait a few minutes (Snowflake may take time to write files)
- Check the correct S3 prefix: `database.schema.tablename/`
- Verify INSERT statements succeeded

### **"Sample data insertion failed"**
**Problem:** Data type mismatch or constraint violation

**Solution:**
- Check your column data types are valid
- Ensure no NOT NULL constraints on sample data
- Verify table was created successfully first

## 🌐 Network Issues

### **"Connection timeout" or "Network unreachable"**
**Problem:** Network connectivity issues

**Solution:**
1. Check internet connection
2. Verify firewall allows outbound HTTPS (443)
3. If behind corporate proxy, configure:
```bash
export HTTPS_PROXY=your-proxy:port
export HTTP_PROXY=your-proxy:port
```

### **"SSL certificate verification failed"**
**Problem:** Certificate issues (common in corporate environments)

**Solution:**
```bash
# Temporary fix (not recommended for production)
export PYTHONHTTPSVERIFY=0
```

## 🖥️ Streamlit Issues

### **"Port 8501 is already in use"**
**Problem:** Another Streamlit app is running

**Solution:**
```bash
# Kill existing Streamlit processes
pkill -f streamlit
# Or run on different port
streamlit run Iceberg_Table_Creator.py --server.port 8502
```

### **"Module not found" errors**
**Problem:** Dependencies not installed properly

**Solution:**
```bash
# Reinstall requirements
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

## 🐛 General Debugging

### **Enable Debug Mode**
Add this to the top of `Iceberg_Table_Creator.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Check Streamlit Logs**
Streamlit shows errors in the terminal where you ran it. Check for:
- Import errors
- Connection failures
- Permission issues

### **Clear Streamlit Cache**
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache
# Or in the app
# Settings → Clear Cache
```

## 📞 Getting Help

If you're still stuck:

1. **Check the logs** in your terminal
2. **Search existing issues** on GitHub
3. **Create a new issue** with:
   - Error message (full traceback)
   - Your OS and Python version
   - Steps to reproduce
   - Relevant config (remove sensitive data!)

## 💡 Pro Tips

- **Test connections separately** before running the full setup
- **Use unique names** for AWS resources to avoid conflicts
- **Keep credentials secure** and never commit them to git
- **Run in a clean virtual environment** to avoid package conflicts
- **Check AWS/Snowflake quotas** if you hit limits

---

**Still need help?** [Open an issue](https://github.com/your-username/iceberg-table-creator/issues) and we'll help you out! 🚀
