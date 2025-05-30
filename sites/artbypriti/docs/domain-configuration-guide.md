# GitHub Pages Domain Configuration Guide

This document outlines the complete process for configuring a custom domain for a Hugo site hosted on GitHub Pages.

## Overview

When setting up a custom domain for your GitHub Pages site, there are several components that need to be configured correctly:

1. DNS Configuration (at your domain provider)
2. GitHub Pages settings
3. Hugo configuration
4. Repository CNAME file

## Step 1: Purchase a Domain

If you don't already have a domain, purchase one from a domain registrar like:
- Namecheap
- GoDaddy
- Google Domains
- Squarespace
- etc.

## Step 2: Configure DNS Records

Log in to your domain provider's dashboard and locate the DNS management section. You'll need to add the following records:

### A Records

Add four A records for the apex domain (e.g., `artbypriti.com`):

```
Type  Host/Name  Value/Points to     TTL
A     @          185.199.108.153     (Default/Automatic)
A     @          185.199.109.153     (Default/Automatic)
A     @          185.199.110.153     (Default/Automatic)
A     @          185.199.111.153     (Default/Automatic)
```

> **Important**: Delete any existing A records for the apex domain that point to different IP addresses.

### CNAME Record

Add a CNAME record for the `www` subdomain:

```
Type   Host/Name  Value/Points to          TTL
CNAME  www        your-github-username.github.io  (Default/Automatic)
```

### Special Notes for Squarespace Domains

If you're using Squarespace as your domain provider:

1. In Squarespace, navigate to **Domains** > **[Your Domain]** > **DNS Settings**
2. Under **Custom Records**, add all four A records and the CNAME record as mentioned above
3. Squarespace may show these records under "Squarespace Domain Connect" - make sure to use "Custom Records" instead
4. If you see your domain using Squarespace nameservers (ns-cloud-c1.googledomains.com, etc.), your DNS changes might take longer to propagate

For our site, this would be:
```
CNAME  www        gadjoy.github.io
```

> **Note**: Do NOT include the repository name in the CNAME value.

## Step 3: Configure GitHub Repository Settings

1. Go to your GitHub repository (e.g., github.com/gadjoy/artbypriti)
2. Navigate to Settings > Pages
3. Under "Custom domain", enter your domain (e.g., `artbypriti.com`)
4. Click "Save"
5. Once DNS propagation is complete, check "Enforce HTTPS" (this might take up to 24 hours to become available)

## Step 4: Add CNAME File to Your Repository

GitHub Pages requires a CNAME file at the root of your published site. For Hugo, this file should be placed in the `static` folder:

```
/static/CNAME
```

The content should be just your domain name without any protocol or trailing slash:

```
artbypriti.com
```

## Step 5: Update Hugo Configuration

Update your `hugo.toml` (or `config.toml`) file to use your custom domain:

```toml
baseURL = 'https://artbypriti.com/'
languageCode = 'en-us'
title = 'Art by Priti'
theme = 'gallery'

[taxonomies]
  category = "categories"
```

## Step 6: Wait for DNS Propagation

DNS changes can take time to propagate across the internet:
- Minimum: A few hours
- Average: 24 hours
- Maximum: Up to 48 hours

During this period, you might see an error in GitHub Pages settings: "Domain does not resolve to the GitHub Pages server." This is normal while DNS is propagating.

## Step 7: Verify DNS Propagation

You can check if your DNS settings have propagated using the `dig` command in terminal:

```zsh
# Check apex domain
dig artbypriti.com +noall +answer

# Check www subdomain
dig www.artbypriti.com +noall +answer
```

When properly configured, the apex domain should return GitHub Pages IP addresses (185.199.108.153, etc.), and the www subdomain should have a CNAME pointing to your GitHub Pages domain.

If you see old IP addresses, your DNS changes haven't fully propagated yet.

## Step 8: Clear Local DNS Cache

If you're still seeing old results, you might need to clear your local DNS cache:

```zsh
# For macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

## Step 9: Verify Domain Configuration Thoroughly

To ensure your domain is properly configured for GitHub Pages and HTTPS:

### Check DNS Records Using Online Tools

Use a service like [DNS Checker](https://dnschecker.org/) or [MX Toolbox](https://mxtoolbox.com/DNSLookup.aspx) to verify your DNS records have propagated globally:

1. Check your A records for the apex domain
2. Check your CNAME record for the www subdomain

### Verify Certificate Eligibility

GitHub Pages uses Let's Encrypt to issue certificates. Ensure your domain doesn't have CAA records preventing Let's Encrypt from issuing certificates:

```zsh
# Check for CAA records
dig CAA artbypriti.com
```

If there are CAA records, they should either be absent or include Let's Encrypt (`letsencrypt.org`).

### Force GitHub Pages to Recheck Your Domain (Use Cautiously)

Sometimes GitHub Pages needs encouragement to recheck your DNS settings, but only use this if you're experiencing ongoing issues:

1. Temporarily remove your custom domain from GitHub Pages settings
2. Save the settings
3. Add your custom domain back
4. Save again

**Note:** Only use this method as a last resort if your DNS verification has been successful for over 48 hours and HTTPS still isn't available. If your DNS has just recently become verified, it's better to wait for GitHub's automatic certificate issuance process to complete naturally (typically 24-48 hours after DNS verification).

## Common Issues and Solutions

### Error: "Domain does not resolve to the GitHub Pages server"

**Cause**: DNS settings haven't propagated yet, or DNS is misconfigured.

**Solution**: 
- Double-check DNS settings, especially A records
- Wait longer for propagation
- Verify with `dig` command

### Error: "Domain is not properly configured"

**Cause**: The CNAME file in your repository is missing or incorrect.

**Solution**: Ensure the CNAME file is in the `static` directory and contains only your domain name.

### HTTPS Not Available

**Cause**: DNS propagation not complete, or certificate not yet issued.

**Solution**: Wait 24 hours after DNS propagation completes, then check "Enforce HTTPS" option.

### Persistent "Domain not properly configured" Error

If your site is online but GitHub Pages still displays "Domain not properly configured" and HTTPS is unavailable:

**Potential Causes**:
1. **DNS Not Fully Propagated**: Even though the site is accessible, DNS might not be fully resolved for all GitHub's validation servers.
2. **Nameserver Issues**: If you're using custom nameservers (like Squarespace's), GitHub's verification might have trouble.
3. **CAA Records**: If your domain has CAA (Certificate Authority Authorization) records that don't include GitHub's CA.
4. **DNS Caching**: GitHub might be caching your previous DNS settings.

**Solutions**:
1. Wait another 24-48 hours for full propagation
2. Try temporarily switching to your domain registrar's default nameservers instead of Squarespace's
3. Verify your records with an online DNS lookup tool like https://mxtoolbox.com/DNSLookup.aspx
4. Contact GitHub Support if issues persist after 48 hours

## Special Considerations for Squarespace Domains

If you purchased your domain through Squarespace or are using Squarespace nameservers:

### Nameserver vs. DNS Record Approach

Squarespace provides two ways to configure your domain for GitHub Pages:

1. **DNS Records Approach** (Recommended): Keep using Squarespace nameservers but add custom DNS records for GitHub Pages.
   - Easier to maintain if you're also using Squarespace for email or other services
   - May require longer propagation time (up to 72 hours in some cases)
   
2. **Nameserver Switch**: Change from Squarespace's nameservers to nameservers offered by your domain registrar.
   - More direct control over DNS
   - May resolve GitHub Pages verification issues
   - Requires more technical setup
   
### Squarespace-Specific Troubleshooting

If you've properly configured all DNS records but still encounter issues:

1. In Squarespace, verify you're using "Custom Records" (not "Automatic")
2. Try temporarily deactivating any Squarespace services for the domain
3. If possible, transfer management of the domain's DNS to your registrar instead of using Squarespace's nameservers
4. If using Squarespace Email, be aware this may require additional configuration to maintain email services

### When to Contact Support

If after 72 hours your GitHub Pages still shows as improperly configured:
1. Contact Squarespace support to verify they're not blocking GitHub's verification process
2. Contact GitHub support with proof of your DNS configuration

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Troubleshooting Custom Domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages)
- [Hugo Documentation](https://gohugo.io/hosting-and-deployment/hosting-on-github/)
- [Squarespace Domain Management](https://support.squarespace.com/hc/en-us/articles/205812378-Connecting-a-domain-to-your-Squarespace-site)
- [Let's Encrypt CAA Information](https://letsencrypt.org/docs/caa/)
