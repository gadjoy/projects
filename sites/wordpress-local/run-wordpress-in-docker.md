# Installing Wordpress Docker style

## **Overview**

This guide covers the process of **migrating a WordPress website** using **All-in-One WP Migration** and **increasing the upload file size limit** inside a Docker-based WordPress environment.

---

## **Step 1: Setup WordPress in Docker**

1. Ensure your **Docker Compose setup** is running:

   ```bash
   docker-compose up -d
   ```

2. Access WordPress at:

   ```link
   http://localhost:8080
   ```

3. Install the **All-in-One WP Migration** plugin.

---

## **Step 2: Export WordPress Website**

1. In the WordPress dashboard, go to:

   ```instruction
   All-in-One WP Migration > Export
   ```

2. Choose **File** and click **Export**.
3. Download the `.wpress` file to your local system.

---

## **Step 3: Increase WordPress Upload Limit**

By default, WordPress in Docker has a **low upload file size limit**, preventing large `.wpress` files from being imported.

### **Method 1: Modify `.htaccess` (Recommended)**

1. Open **VS Code** and install the **Docker extension**.
2. Open the **WordPress container** from VS Code and navigate to:

   ```path
   /var/www/html/.htaccess
   ```

3. Edit `.htaccess` and add:

   ```apache
   php_value upload_max_filesize 512M
   php_value post_max_size 512M
   php_value memory_limit 256M
   php_value max_execution_time 300
   php_value max_input_time 300
   ```

4. Save the file.

---

## **Step 4: Restart the Docker Container**

1. Find the **WordPress container name**:

   ```bash
   docker ps
   ```

2. Restart the container:

   ```bash
   docker restart wordpress-container
   ```

---

## **Step 5: Verify Upload Limit**

1. In WordPress, navigate to:

   ```
   Media > Add New
   ```

2. Check if the **upload limit** has increased.

---

## **Step 6: Import the `.wpress` File**

1. Go to **All-in-One WP Migration > Import**.
2. Select the `.wpress` file and upload it.
3. Wait for the process to complete.
4. Verify that your site is restored successfully.

---

## **Done! 🎉**

Your WordPress site has been **successfully migrated and restored** inside Docker with an **increased upload limit**.
