# Aa OCR parsing demo with usage of PydanticAI

## MacOS users

```bash
# Package used by `pdf2image`
brew install poppler
```

### `1_basic_ocr_demo.py` example output

```markdown
# Invoice

YesLogic Pty. Ltd.
7 / 39 Bouverie St
Carlton VIC 3053
Australia

[www.yeslogic.com](http://www.yeslogic.com)
ABN 32 101 193 560

---

Customer Name
Street
Postcode City
Country

**Invoice date:** Nov 26, 2016
**Invoice number:** 161126
**Payment due:** 30 days after invoice date

| Description                 | From       | Until      | Amount     |
|-----------------------------|------------|------------|------------|
| Prince Upgrades & Support   | Nov 26, 2016 | Nov 26, 2017 | USD $950.00 |
| **Total**                   |            |            | USD $950.00 |

---

Please transfer amount to:

**Bank account name:** Yes Logic Pty Ltd
**Name of Bank:** Commonwealth Bank of Australia (CBA)
**Bank State Branch (BSB):** 063010
**Bank State Branch (BSB):** 063010
**Bank State Branch (BSB):** 063019
**Bank account number:** 13201652
**Bank SWIFT code:** CTBAAU2S
**Bank address:** 231 Swanston St, Melbourne, VIC 3000, Australia

*The BSB number identifies a branch of a financial institution in Australia. When transferring money to Australia, the BSB number is used together with the bank account number and the SWIFT code. Australian banks do not use IBAN numbers.*

---

[www.yeslogic.com](http://www.yeslogic.com)
```

### Files samples

All the filed were downloaded from [Prince XML](https://www.princexml.com/samples/)

``markdown
[Sunny Farm Logo](image-url-placeholder)

# ATTENTION TO
**Denny Gunawan**

221 Queen St
Melbourne VIC 3000

## $39.60

---

## Sunny Farm Victoria

123 Somewhere St, Melbourne VIC 3000
(03) 1234 5678

Invoice Number: **#20130304**

---

| Organic Items | Price/kg | Quantity(kg) | Subtotal |
|---------------|----------|--------------|----------|
| Apple         | $5.00    | 1            | $5.00    |
| Orange        | $1.99    | 2            | $3.98    |
| Watermelon    | $1.69    | 3            | $5.07    |
| Mango         | $9.56    | 2            | $19.12   |
| Peach         | $2.99    | 1            | $2.99    |

---

### THANK YOU

* Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam sodales dapibus fermentum. Nunc adipiscing, magna sed scelerisque cursus, erat lectus dapibus urna, sed facilisis leo dui et ipsum.

---

|                |          |
|----------------|----------|
| **Subtotal**   | $36.00   |
| **GST (10%)**  | $3.60    |
| **Total**      | **$39.60** |



```
