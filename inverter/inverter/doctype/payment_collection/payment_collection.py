# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentCollection(Document):

	def on_submit(self):
		email_ids = frappe.db.sql("select email_id from `tabEmail Recipients` where parent='Support Setup'",as_dict=1)
		email_list = [item['email_id'] for item in email_ids]
		payment_date = frappe.utils.formatdate(self.date, "dd-MM-yyyy")

		message = f"""Dear {self.customer},<br><br>

		We are pleased to inform you that your payment has been successfully completed.<br><br>

		<strong>Transaction Details:</strong>
		<ul>
			<li><strong>Amount Paid:</strong> {self.grand_total}</li>
			<li><strong>Date:</strong> {self.date}</li>
		</ul>"""

		table_rows = ""
		if self.payments:
			# Fetch data for each payment ID
			for payment_id in self.payments:
				try:
					print(payment_id)
				
					item_code = payment_id.item_code or "-"
					quantity = payment_id.quantity or 0  # Default to 0 if None
					amount = payment_id.amount or 0  # Default to 0 if None
					remarks = payment_id.remarks or ""
					table_rows += f"""
						<tr style="border: 1px solid #ddd;">
							<td style="border: 1px solid #ddd; padding: 8px;">{item_code}</td>
							<td style="border: 1px solid #ddd; padding: 8px;">{quantity}</td>
							<td style="border: 1px solid #ddd; padding: 8px;">{amount}</td>
							<td style="border: 1px solid #ddd; padding: 8px;">{remarks}</td>
						</tr>
					"""
				except frappe.DoesNotExistError:
					# Skip if the payment ID is not found
					continue

			# Add the table only if rows exist
			if table_rows:
				table_html = f"""
								<br>
								<div style="width: 100%; clear: both;">
									<h3 style="font-family: Arial, sans-serif; color: #333;">Payments</h3>
									<table style="border: 1px solid #ddd; border-collapse: collapse; width: 50%; font-family: Arial, sans-serif; font-size: 14px; text-align: left; float: left;">
										<thead style="background-color: #f2f2f2; color: #333;">
											<tr style="border: 1px solid #ddd;">
												<th style="border: 1px solid #ddd; padding: 8px;">Item Code</th>
												<th style="border: 1px solid #ddd; padding: 8px;">Qty</th>
												<th style="border: 1px solid #ddd; padding: 8px;">Amount</th>
												<th style="border: 1px solid #ddd; padding: 8px;">Remarks</th>
											</tr>
										</thead>
										<tbody>
											{table_rows}
										</tbody>
									</table>
								</div>
								<br>
								<br>
							"""
				message += table_html

			pending_table_rows = ""
			if self.pending_payment_collection:
				# Fetch data for each payment ID
				for payment_id in self.pending_payment_collection:
					try:
						item = payment_id.item or ""
						remarks = payment_id.remarks or ""
						amount = payment_id.amount or 0  # Default to 0 if None
						pending_table_rows += f"""
							<tr style="border: 1px solid #ddd;">
								<td style="border: 1px solid #ddd; padding: 8px;">{item}</td>
								<td style="border: 1px solid #ddd; padding: 8px;">{amount}</td>
								<td style="border: 1px solid #ddd; padding: 8px;">{remarks}</td>
							</tr>
						"""
					except frappe.DoesNotExistError:
						# Skip if the payment ID is not found
						continue

				# Add the table only if rows exist
				if pending_table_rows:
					pending_payment = f"""
										<br>
										<br>
										<div style="width: 100%; clear: both;">
											<h3 style="margin-top:30px; color: #333;">Pending Payments</h3>
											<table style="border: 1px solid #ddd; border-collapse: collapse; width: 50%; font-family: Arial, sans-serif; font-size: 14px; text-align: left; float: left;">
												<thead style="background-color: #f2f2f2; color: #333;">
													<tr style="border: 1px solid #ddd;">
													    <th style="border: 1px solid #ddd; padding: 8px;">Item Code</th>
													    <th style="border: 1px solid #ddd; padding: 8px;">Amount</th>
														<th style="border: 1px solid #ddd; padding: 8px;">Remarks</th>
														
													</tr>
												</thead>
												<tbody>
													{pending_table_rows}
												</tbody>
											</table>
										</div>
										<br>
										"""
					message += pending_payment

		



		admin_message = f"""Dear Sir/Madam,<br><br>

						This is to inform you that the payment has been successfully processed.<br><br>

						<strong>Details:</strong>
						<ul>
							<li><strong>Transaction ID:</strong> {self.name}</li>
							<li><strong>Payment Date:</strong> {payment_date}</li>
							<li><strong>Amount:</strong> {self.grand_total}</li>
							<li><strong>Paid By:</strong> {self.customer}</li>
						</ul>


						"""
		
		if self.payments:
			admin_message += table_html
					
		if self.pending_payment_collection:
			admin_message += pending_payment



		try:
			frappe.sendmail(
				recipients= self.customer_email_id,  
				subject=frappe._('Payment Confirmation'),
				message=message
			)


			frappe.sendmail(
				recipients=email_list,  
				subject=frappe._('Payment Confirmation'),
				message=admin_message
			)
			
			frappe.email.queue.flush()
			
		except frappe.OutgoingEmailError as e:
			frappe.log_error(message=str(e), title="Email Sending Failed")