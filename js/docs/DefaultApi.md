# LetsrolldApi.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**directorsGet**](DefaultApi.md#directorsGet) | **GET** /directors | Get Directors
[**directorsIdGet**](DefaultApi.md#directorsIdGet) | **GET** /directors/{id} | Get Director
[**filmsGet**](DefaultApi.md#filmsGet) | **GET** /films | Get Films
[**filmsIdGet**](DefaultApi.md#filmsIdGet) | **GET** /films/{id} | Get Film



## directorsGet

> [Object] directorsGet(opts)

Get Directors

### Example

```javascript
import LetsrolldApi from 'letsrolld_api';

let apiInstance = new LetsrolldApi.DefaultApi();
let opts = {
  'limit': 10 // Number | Number of directors to return
};
apiInstance.directorsGet(opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **Number**| Number of directors to return | [optional] [default to 10]

### Return type

**[Object]**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## directorsIdGet

> Director directorsIdGet(id)

Get Director

### Example

```javascript
import LetsrolldApi from 'letsrolld_api';

let apiInstance = new LetsrolldApi.DefaultApi();
let id = 56; // Number | id
apiInstance.directorsIdGet(id, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| id | 

### Return type

[**Director**](Director.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## filmsGet

> [Object] filmsGet(opts)

Get Films

### Example

```javascript
import LetsrolldApi from 'letsrolld_api';

let apiInstance = new LetsrolldApi.DefaultApi();
let opts = {
  'limit': 10, // Number | Number of films to return
  'genre': "genre_example", // String | Genre to filter by
  'country': "country_example", // String | Country to filter by
  'offer': "offer_example" // String | Offer to filter by
};
apiInstance.filmsGet(opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **Number**| Number of films to return | [optional] [default to 10]
 **genre** | **String**| Genre to filter by | [optional] 
 **country** | **String**| Country to filter by | [optional] 
 **offer** | **String**| Offer to filter by | [optional] 

### Return type

**[Object]**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## filmsIdGet

> Film filmsIdGet(id)

Get Film

### Example

```javascript
import LetsrolldApi from 'letsrolld_api';

let apiInstance = new LetsrolldApi.DefaultApi();
let id = 56; // Number | id
apiInstance.filmsIdGet(id, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| id | 

### Return type

[**Film**](Film.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

