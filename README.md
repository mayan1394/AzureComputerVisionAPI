# AzureComputerVisionAPI Set up

#Before using the Azure Computer Vision API, you will have to create a free account on Azure and then configure environment variables on your system using the "keys" and "endpoints" generated from it. Please find detailed process listed below.

#Navigate to Cognitive Services on Azure and then to Marketplace. Search for Computer Vision in Market Place and then create a subscription for it. You will have to assign this subscription to a resource group. If a resource group is not created beforehand, you will have to create a new one. In instance details - select a region which is near to the place where you will be accessing the service. This will reduce the chances of any lag issues.In the Pricing Tier, make sure that you select the Free tier. Create the subscription.

#Navigate to the resource group which you create and go to the "Resource Management" section. You will find Keys and Endpoints here. Either of Key1 or Key2 can be used to access Vision API programmatically from your system.I am attaching a requirements file, which you can use to install relevant packages. You should use the command below to achieve this - pip install -r requirements.txt

#Create enviornment variables on your system(for Windows), Go to Command Prompt and write these commands-
setx COMPUTER_VISION_SUBSCRIPTION_KEY "your-key"
setx COMPUTER_VISION_ENDPOINT "your-emdpoint"


#Then, create variables for your resource's Azure endpoint and key
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
