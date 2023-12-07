# BillingCustomer

A billable customer assigned to one or more organisations.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The customer&#39;s full name or business name. | [optional] 
**email** | **str** | The customer&#39;s email address | [optional] 
**balance** | **int** | The current balance, if any, that’s stored on the customer. If negative, the customer has credit to apply to their next invoice. If positive, the customer has an amount owed that’s added to their next invoice. The balance only considers amounts that Stripe hasn’t successfully applied to any invoice. It doesn’t reflect unpaid invoices. This balance is only taken into account after invoices finalize.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


