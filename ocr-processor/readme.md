# Handwriting OCR for Apartment Maintenance Expenses

This project uses Google Cloud Vision API to extract handwritten text from images of apartment maintenance expense entries.

## Prerequisites

- Python 3.7 or higher
- A Google Cloud account (free tier available with $300 credits)

## Setup Instructions

### 1. Install Google Cloud CLI

#### For Windows (Recommended Method):

**Download and Install:**
1. Download the Windows installer (64-bit): https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
2. Run the installer (`GoogleCloudSDKInstaller.exe`)
3. Follow the installation wizard:
   - Accept the terms
   - Choose installation directory (default is fine)
   - Check "Start Cloud SDK Shell" and "Run 'gcloud init'" options
4. The installer will open a Cloud SDK Shell window automatically

**Alternative - Manual Installation:**
1. Download: https://dl.google.com/dl/cloudsdk/channels/rapid/google-cloud-cli-windows-x86_64-bundled-python.zip
2. Extract the ZIP file to `C:\Program Files\Google\Cloud SDK\`
3. Run `google-cloud-sdk\install.bat` from the extracted folder
4. Restart your terminal/command prompt

**Verify Installation:**
Open a **new** PowerShell or Command Prompt window and run:
```cmd
gcloud --version
```

You should see output showing the SDK version.

#### For macOS:
```bash
# Using Homebrew
brew install --cask google-cloud-sdk

# Or using the installer
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

#### For Linux:
```bash
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install
sudo apt-get update && sudo apt-get install google-cloud-cli
```

### 2. Initialize Google Cloud CLI and Login

**Open a new PowerShell or Command Prompt window** and run:

```cmd
gcloud init
```

Follow the prompts to:
1. Login to your Google account (browser will open)
2. Select or create a Google Cloud project with id "osrprocessor20251029"

**Note for Windows users:** If you see any errors, try running as Administrator or use the "Cloud SDK Shell" that was installed with the SDK.

### 3. List Projects
1. Ensure you see the project created in step 2. 

```bash
# List all projects to verify
gcloud projects list
```

### 4. Set the Current Project

```bash
# Set your active project
gcloud config set project osrprocessor20251029

# Verify the current project
gcloud config get-value project
```

### 5. Enable the Vision API

```bash
# Enable Cloud Vision API
gcloud services enable vision.googleapis.com

# Verify the API is enabled
gcloud services list --enabled | grep vision
```

### 6. Create a Service Account

```bash
# Create a service account
gcloud iam service-accounts create sa-ocr-processor \
    --display-name="Handwriting OCR Service Account" \
    --description="Service account for handwriting OCR processing"

# Verify 'sa-ocr-processor' service account creation
gcloud iam service-accounts list
```

### 7. Grant Necessary Permissions to Service Account

**For Development/Testing (Broader Access):**

```bash
# Get your project ID
PROJECT_ID=$(gcloud config get-value project)

# Grant the ML Admin role to the service account (broader access for development)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:sa-ocr-processor@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/ml.admin"

# Verify the role binding
gcloud projects get-iam-policy $PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:sa-ocr-processor@${PROJECT_ID}.iam.gserviceaccount.com"
```
### 8. Download Service Account Credentials

```bash
# Create a key for the service account and download as JSON
gcloud iam service-accounts keys create credentials.json \
    --iam-account=sa-ocr-processor@${PROJECT_ID}.iam.gserviceaccount.com

# This will create a 'credentials.json' file in your current directory
```

### 9. Set Environment Variable for Authentication
Run this step in our vs-code editor console
#### For Windows (Command Prompt):
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=%CD%\credentials.json

# Or To set it permenantly
setx GOOGLE_APPLICATION_CREDENTIALS "%CD%\credentials.json"
```
#### For Windows (PowerShell):
```cmd
$env:GOOGLE_APPLICATION_CREDENTIALS="$PWD\credentials.json"
# Or To set it permenantly
[System.Environment]::SetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', "$PWD\credentials.json", 'User')
```

### 10. Google Billing: 

You need to enable billing on your Google Cloud project. Don't worry - you won't be charged if you stay within the free tier, and new accounts get $300 in free credits. Then run 
```
# List available billing accounts
gcloud billing accounts list

# Link billing account to your project
gcloud billing projects link PROJECT_ID \
    --billing-account=BILLING_ACCOUNT_ID
```

### 11. Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```


## Usage

### 1. Prepare Your Images

Create an `images` directory then copy all your handwritten images here. 
```bash
mkdir images
```
### 2. Run the OCR Script
```bash
python.exe ocr_processor.py
```

The script will:
- Process all images in the `images/` directory
- Use Google Cloud Vision API's `DOCUMENT_TEXT_DETECTION` feature
- Extract full text from each image
- Save results as `.txt` files in the `text/` directory
- Each output file will have the same name as the input image (with `.txt` extension)

## Security Notes

⚠️ **IMPORTANT**: 
- Never commit `credentials.json` to version control
- Add `credentials.json` to your `.gitignore` file
- Keep your service account keys secure
- Delete unused service account keys from Google Cloud Console

## Additional Resources

- [Google Cloud Vision API Documentation](https://cloud.google.com/vision/docs)
- [Vision API Pricing](https://cloud.google.com/vision/pricing)
- [Best Practices for Authentication](https://cloud.google.com/docs/authentication/best-practices)

## License
This project is for personal use. Ensure compliance with Google Cloud's terms of service.