# Best-Buy-Retail-Store-P.O.S-sytem
point of sale system for Best Buy Retail Store 

Authors:  Ashanti Allen & Shemar Cameron

 Date Created: April 2, 2026
 
 Course:       ITT103 - Programming Techniques
 
 Purpose:      Point of Sale (POS) System for Best Buy Retail Store
 
 GitHub URL: 
  https://github.com/scameron22-crypto/Best-Buy-Retail-Store-P.O.S-sytem.git
  https://github.com/aallen60/Best-Buy-Retail-Store-P.O.S-system.git

 Purpose:
   This program simulates a Point of Sale system allowing cashiers
   to manage a product catalog, process customer purchases, apply
   taxes and discounts, accept payments, and generate receipts.

 How to Run:
   Execute this file with Python 3: python DigitalDynamos-POS-ITT103-SP2026.py

 Assumptions / Limitations:
   - Prices are in Jamaican Dollars (JMD).
   - A 10% sales tax is applied to all transactions.
   - A 5% discount is applied when the subtotal exceeds $5000.
   - Stock is updated after each completed transaction.
   - Low-stock alert triggers when any item quantity falls below 5.

 "I CERTIFY THAT I HAVE NOT GIVEN OR RECEIVED ANY UNAUTHORIZED
  ASSISTANCE ON THIS ASSIGNMENT"
 ============================================================

 ──────────────────────────────────────────────
 
 PRODUCT CATALOG
 Structure: { product_name: {"price": float, "stock": int} }
