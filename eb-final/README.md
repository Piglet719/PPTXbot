# Follow the instructions to deploy on AWS(using elastic beanstalk and cloudfront)

## Elastic Beanstalk

1. **Navigate to Elastic Beanstalk:**

   - Go to the AWS Management Console and navigate to Elastic Beanstalk.

2. **Create Application:**

   - Click on "Create Application".
   - For the Environment tier, choose "Web server environment".
   - Fill in the required information:
     - **Application name:** Specify a name for your application.
     - **Environment information:** Enter details such as environment name, domain, etc.

3. **Configure Environment:**

   - Under Platform, select "Python".
   - For Application code, choose "Upload your code" and upload the "eb7-final_ver.zip" file located in the root directory.

4. **Review Configuration:**

   - Leave other settings as default, or adjust them according to your requirements.

5. **Deploy Application:**

   - Review your configuration settings.
   - Click on "Create application" to deploy your application on Elastic Beanstalk.

6. **Retrieve Elastic Beanstalk URL:**

   - Once the deployment is complete, retrieve the Elastic Beanstalk URL link provided in the Elastic Beanstalk dashboard.

7. **Substitute Backend Files:**

   - Use the Elastic Beanstalk URL link to substitute frontend files(under eb/frontend1) or configure your application as needed.

8. **Upload Zipped File:**
   - Use the following command to zip your files again:
     ```
     zip -r eb7-final_ver.zip . -x '*virt*' -x '*frontend1*' -x '*eb*'
     ```
   - This command recursively zips all files in the current directory, excluding those with names containing 'virt', 'frontend1', and 'eb'.

## S3 Bucket Configuration

1. **Navigate to S3:**

   - Go to the AWS Management Console and navigate to the S3 service.

2. **Build Frontend:**

   - Navigate to the 'frontend1' directory and run the command:
     ```
     npm run build
     ```
   - This command will generate a 'dist' folder containing the built frontend files.

3. **Create Bucket and Upload Files:**

   - Create a new S3 bucket.
   - Upload all files and folders from the 'frontend1/dist' directory into the newly created bucket.

4. **Configure Bucket Permissions:**

   - Configure the bucket policy to allow public read access to the objects. This ensures that the frontend files can be accessed by anyone.
   - Go to the bucket properties and navigate to the permissions tab. Then, add a bucket policy similar to the following:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Sid": "PublicReadGetObject",
           "Effect": "Allow",
           "Principal": "*",
           "Action": ["s3:GetObject", "s3:PutObject"],
           "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
         }
       ]
     }
     ```
   - Replace `YOUR_BUCKET_NAME` with the name of your S3 bucket.
   - Navigate to Cross-Origin Resource Sharing (CORS), and add the following CORS configuration:

     ```json
     [
       {
         "AllowedHeaders": ["*"],
         "AllowedMethods": ["GET", "HEAD", "POST", "PUT", "DELETE"],
         "AllowedOrigins": ["*"],
         "ExposeHeaders": ["ETag"]
       }
     ]
     ```

5. **Enable Static Website Hosting:**

   - After creating the bucket, go to the bucket properties and choose "Static website hosting."
   - Select "Use this bucket to host a website" and specify the index document (for this case: index.html).
   - Save the configuration.

6. **Retrieve S3 Bucket URL:**
   - Once the files are uploaded and permissions are configured, retrieve the S3 bucket URL. This URL will be used to access the frontend of your application.

## Cloudfront Setup

1. Navigate to the AWS CloudFront console and select "Create Distribution".
2. Choose the domain created by Elastic Beanstalk as the origin for your CloudFront distribution.
3. Ensure that the "Viewer Protocol Policy" includes both HTTP and HTTPS, and set the "Allowed HTTP Methods" to include "GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE" since we did not apply for an SSL certificate.
4. For cache policy, choose "Cache Optimized" to optimize caching behavior.

## Accessing the Website

After setting up CloudFront, you can access your website by navigating to the CloudFront URL provided. Simply click on the CloudFront link, and it will display your website.
