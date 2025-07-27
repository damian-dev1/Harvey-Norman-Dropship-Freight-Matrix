# Harvey Norman Dropship Freight Matrix Upload Guide

**Version:** 1.0  
**Last Updated:** 2025-07-27  
**Owner:** Dropship Operations  
**Author:** Damian Damjanovic  
**Audience:** Dropship Team, Marketplace Vendors, Integration Developers

* * *

## Overview

This document outlines the official data model, CSV format, validation schema, and operational process for uploading **freight rate data** into the **Azure Cosmos DB** for use by the Dropship API (`/soh/dropship`) and the **Harvey Norman** website.

Freight rates are uploaded by the Dropship team and made available for real-time lookups and frontend caching by Magento.

* * *

## Data Model

Each record in the Freight Matrix contains the following fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `postCode` | string | ✅ Yes | 4-digit Australian postcode |
| `productCode` | string | ✅ Yes | Internal product SKU (max 15 characters) |
| `price` | number | ✅ Yes | Freight price in AUD |
| `id` | string | ✅ Yes | Composite key: `productCode + postCode` |
| `message` | string | ❌ No | Optional message (e.g., zone notes or restrictions) |

### `id` Rule:

Must be the exact concatenation of `productCode` and `postCode`  
Example:

```text
productCode = "SKU123", postCode = "2000" → id = "SKU1232000"
```

* * *

## CSV Upload Format

- File must be in **UTF-8 encoding**
- Header row must be **unquoted**
- All data rows must be **wrapped in double quotes**
- No trailing commas or blank lines

### Valid Example

```csv
postCode,productCode,price,id,message
"2000","SKU123","15.95","SKU1232000",""
"3000","TV-SNY-100","25.00","TV-SNY-1003000","Metro"
"5000","FRIDGE-LG-01","40.00","FRIDGE-LG-015000","Zone 2"
```

* * *

## JSON Schema (Validation Rules)

Before ingesting data, each row must conform to the following [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/damian-dev1/Harvey-Norman-Dropship-Freight-Matrix/freight-matrix-upload-schema.json",
  "title": "FreightRateRecord",
  "type": "object",
  "required": ["postCode", "productCode", "price", "id"],
  "properties": {
    "postCode": {
      "type": "string",
      "pattern": "^\\d{4}$"
    },
    "productCode": {
      "type": "string",
      "minLength": 1,
      "maxLength": 15
    },
    "price": {
      "type": "number",
      "minimum": 0
    },
    "id": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_-]{1,15}\\d{4}$"
    },
    "message": {
      "type": "string",
      "default": ""
    }
  },
  "additionalProperties": false
}
```

> ℹ️ This schema may be enforced by internal tooling, validation middleware, or pre-upload scripts.

* * *

## Operational Workflow

| Step | Description |
| --- | --- |
| 1\. Receive | Freight CSV is received from Marketplace Vendor |
| 2\. Validate | Data is validated against the schema (see above) |
| 3\. Upload | File is uploaded into Azure Cosmos DB using internal Dropship tooling |
| 4\. Live API | Data becomes immediately available via the `POST /soh/dropship` API |
| 5\. Website | Magento updates its cache and shows rates on frontend within 24 hours |

* * *

## Real-Time Rate Lookup API (`/soh/dropship`)

### Sample Request

```json
[
  { "productCode": "SKU123", "postCode": "2000" },
  { "productCode": "TV-SNY-100", "postCode": "3000" }
]
```

### Sample Response

```json
[
  {
    "deliveryPossible": true,
    "deliveryRate": 15.95,
    "postCode": "2000",
    "productCode": "SKU123"
  },
  {
    "deliveryPossible": true,
    "deliveryRate": 25.00,
    "message": "Metro",
    "postCode": "3000",
    "productCode": "TV-SNY-100"
  }
]
```

* * *

## Storage & Versioning

- All uploaded CSV files must be retained in SharePoint or OneDrive for at least **30 days**
- Filenames should follow this naming convention:  
    `freight_matrix_YYYYMMDD_HHMM.csv`

* * *

## Test Your File

A validation script is available to test uploads locally before pushing to Cosmos DB.

To request access:  
📧 **[damian.damjanovic@au.harveynorman.com](mailto:damian.damjanovic@au.harveynorman.com)**

* * *

## Common Mistakes to Avoid

| Mistake | Fix |
| --- | --- |
| `id` doesn’t match productCode+postCode | Ensure strict concatenation with no delimiter |
| SKU longer than 15 characters | Truncate or request exception approval |
| Missing quotes on data rows | Ensure rows are properly quoted during CSV generation/export |
| Postcode not 4 digits | Validate with regex `^\d{4}$` |
| Price contains `$` symbol | Ensure price is raw number only, no currency symbols |

* * *

## Support

For technical issues, validation errors, or data discrepancies, contact:

**Dropship Technical Support**  
📧 [damian.damjanovic@au.harveynorman.com.au](mailto:damian.damjanovic@au.harveynorman.com)

* * *
