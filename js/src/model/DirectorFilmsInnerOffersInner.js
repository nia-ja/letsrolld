/**
 * letsrolld API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

import ApiClient from '../ApiClient';

/**
 * The DirectorFilmsInnerOffersInner model module.
 * @module model/DirectorFilmsInnerOffersInner
 * @version 0.1
 */
class DirectorFilmsInnerOffersInner {
    /**
     * Constructs a new <code>DirectorFilmsInnerOffersInner</code>.
     * @alias module:model/DirectorFilmsInnerOffersInner
     * @param name {String} 
     * @param monetizationType {String} 
     * @param url {String} 
     */
    constructor(name, monetizationType, url) { 
        
        DirectorFilmsInnerOffersInner.initialize(this, name, monetizationType, url);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, name, monetizationType, url) { 
        obj['name'] = name;
        obj['monetization_type'] = monetizationType;
        obj['url'] = url;
    }

    /**
     * Constructs a <code>DirectorFilmsInnerOffersInner</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/DirectorFilmsInnerOffersInner} obj Optional instance to populate.
     * @return {module:model/DirectorFilmsInnerOffersInner} The populated <code>DirectorFilmsInnerOffersInner</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new DirectorFilmsInnerOffersInner();

            if (data.hasOwnProperty('name')) {
                obj['name'] = ApiClient.convertToType(data['name'], 'String');
            }
            if (data.hasOwnProperty('monetization_type')) {
                obj['monetization_type'] = ApiClient.convertToType(data['monetization_type'], 'String');
            }
            if (data.hasOwnProperty('url')) {
                obj['url'] = ApiClient.convertToType(data['url'], 'String');
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>DirectorFilmsInnerOffersInner</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>DirectorFilmsInnerOffersInner</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of DirectorFilmsInnerOffersInner.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['name'] && !(typeof data['name'] === 'string' || data['name'] instanceof String)) {
            throw new Error("Expected the field `name` to be a primitive type in the JSON string but got " + data['name']);
        }
        // ensure the json data is a string
        if (data['monetization_type'] && !(typeof data['monetization_type'] === 'string' || data['monetization_type'] instanceof String)) {
            throw new Error("Expected the field `monetization_type` to be a primitive type in the JSON string but got " + data['monetization_type']);
        }
        // ensure the json data is a string
        if (data['url'] && !(typeof data['url'] === 'string' || data['url'] instanceof String)) {
            throw new Error("Expected the field `url` to be a primitive type in the JSON string but got " + data['url']);
        }

        return true;
    }


}

DirectorFilmsInnerOffersInner.RequiredProperties = ["name", "monetization_type", "url"];

/**
 * @member {String} name
 */
DirectorFilmsInnerOffersInner.prototype['name'] = undefined;

/**
 * @member {String} monetization_type
 */
DirectorFilmsInnerOffersInner.prototype['monetization_type'] = undefined;

/**
 * @member {String} url
 */
DirectorFilmsInnerOffersInner.prototype['url'] = undefined;






export default DirectorFilmsInnerOffersInner;

