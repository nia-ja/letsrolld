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
 * The ArrayOfDirectors model module.
 * @module model/ArrayOfDirectors
 * @version 0.1
 */
class ArrayOfDirectors extends Array {
    /**
     * Constructs a new <code>ArrayOfDirectors</code>.
     * @alias module:model/ArrayOfDirectors
     * @extends Array
     */
    constructor() { 
        super();
        
        
        ArrayOfDirectors.initialize(this);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj) { 
    }

    /**
     * Constructs a <code>ArrayOfDirectors</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/ArrayOfDirectors} obj Optional instance to populate.
     * @return {module:model/ArrayOfDirectors} The populated <code>ArrayOfDirectors</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new ArrayOfDirectors();

            ApiClient.constructFromObject(data, obj, 'Object');
            

        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>ArrayOfDirectors</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>ArrayOfDirectors</code>.
     */
    static validateJSON(data) {

        return true;
    }


}








export default ArrayOfDirectors;

