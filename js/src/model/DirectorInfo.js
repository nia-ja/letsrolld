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
 * The DirectorInfo model module.
 * @module model/DirectorInfo
 * @version 0.1
 */
class DirectorInfo {
    /**
     * Constructs a new <code>DirectorInfo</code>.
     * @alias module:model/DirectorInfo
     * @param id {Number} 
     * @param name {String} 
     */
    constructor(id, name) { 
        
        DirectorInfo.initialize(this, id, name);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, id, name) { 
        obj['id'] = id;
        obj['name'] = name;
    }

    /**
     * Constructs a <code>DirectorInfo</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/DirectorInfo} obj Optional instance to populate.
     * @return {module:model/DirectorInfo} The populated <code>DirectorInfo</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new DirectorInfo();

            if (data.hasOwnProperty('id')) {
                obj['id'] = ApiClient.convertToType(data['id'], 'Number');
            }
            if (data.hasOwnProperty('name')) {
                obj['name'] = ApiClient.convertToType(data['name'], 'String');
            }
            if (data.hasOwnProperty('lb_url')) {
                obj['lb_url'] = ApiClient.convertToType(data['lb_url'], 'String');
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>DirectorInfo</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>DirectorInfo</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of DirectorInfo.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['name'] && !(typeof data['name'] === 'string' || data['name'] instanceof String)) {
            throw new Error("Expected the field `name` to be a primitive type in the JSON string but got " + data['name']);
        }
        // ensure the json data is a string
        if (data['lb_url'] && !(typeof data['lb_url'] === 'string' || data['lb_url'] instanceof String)) {
            throw new Error("Expected the field `lb_url` to be a primitive type in the JSON string but got " + data['lb_url']);
        }

        return true;
    }


}

DirectorInfo.RequiredProperties = ["id", "name"];

/**
 * @member {Number} id
 */
DirectorInfo.prototype['id'] = undefined;

/**
 * @member {String} name
 */
DirectorInfo.prototype['name'] = undefined;

/**
 * @member {String} lb_url
 */
DirectorInfo.prototype['lb_url'] = undefined;






export default DirectorInfo;

