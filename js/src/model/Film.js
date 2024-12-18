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
import DirectorFilmsInnerCountriesInner from './DirectorFilmsInnerCountriesInner';
import DirectorFilmsInnerOffersInner from './DirectorFilmsInnerOffersInner';
import DirectorInfo from './DirectorInfo';

/**
 * The Film model module.
 * @module model/Film
 * @version 0.1
 */
class Film {
    /**
     * Constructs a new <code>Film</code>.
     * @alias module:model/Film
     * @param title {String} 
     */
    constructor(title) { 
        
        Film.initialize(this, title);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, title) { 
        obj['title'] = title;
    }

    /**
     * Constructs a <code>Film</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/Film} obj Optional instance to populate.
     * @return {module:model/Film} The populated <code>Film</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new Film();

            if (data.hasOwnProperty('id')) {
                obj['id'] = ApiClient.convertToType(data['id'], 'Number');
            }
            if (data.hasOwnProperty('title')) {
                obj['title'] = ApiClient.convertToType(data['title'], 'String');
            }
            if (data.hasOwnProperty('description')) {
                obj['description'] = ApiClient.convertToType(data['description'], 'String');
            }
            if (data.hasOwnProperty('year')) {
                obj['year'] = ApiClient.convertToType(data['year'], 'Number');
            }
            if (data.hasOwnProperty('rating')) {
                obj['rating'] = ApiClient.convertToType(data['rating'], 'String');
            }
            if (data.hasOwnProperty('runtime')) {
                obj['runtime'] = ApiClient.convertToType(data['runtime'], 'Number');
            }
            if (data.hasOwnProperty('lb_url')) {
                obj['lb_url'] = ApiClient.convertToType(data['lb_url'], 'String');
            }
            if (data.hasOwnProperty('jw_url')) {
                obj['jw_url'] = ApiClient.convertToType(data['jw_url'], 'String');
            }
            if (data.hasOwnProperty('trailer_url')) {
                obj['trailer_url'] = ApiClient.convertToType(data['trailer_url'], 'String');
            }
            if (data.hasOwnProperty('genres')) {
                obj['genres'] = ApiClient.convertToType(data['genres'], ['String']);
            }
            if (data.hasOwnProperty('countries')) {
                obj['countries'] = ApiClient.convertToType(data['countries'], [DirectorFilmsInnerCountriesInner]);
            }
            if (data.hasOwnProperty('offers')) {
                obj['offers'] = ApiClient.convertToType(data['offers'], [DirectorFilmsInnerOffersInner]);
            }
            if (data.hasOwnProperty('directors')) {
                obj['directors'] = ApiClient.convertToType(data['directors'], [DirectorInfo]);
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>Film</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>Film</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of Film.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['title'] && !(typeof data['title'] === 'string' || data['title'] instanceof String)) {
            throw new Error("Expected the field `title` to be a primitive type in the JSON string but got " + data['title']);
        }
        // ensure the json data is a string
        if (data['description'] && !(typeof data['description'] === 'string' || data['description'] instanceof String)) {
            throw new Error("Expected the field `description` to be a primitive type in the JSON string but got " + data['description']);
        }
        // ensure the json data is a string
        if (data['rating'] && !(typeof data['rating'] === 'string' || data['rating'] instanceof String)) {
            throw new Error("Expected the field `rating` to be a primitive type in the JSON string but got " + data['rating']);
        }
        // ensure the json data is a string
        if (data['lb_url'] && !(typeof data['lb_url'] === 'string' || data['lb_url'] instanceof String)) {
            throw new Error("Expected the field `lb_url` to be a primitive type in the JSON string but got " + data['lb_url']);
        }
        // ensure the json data is a string
        if (data['jw_url'] && !(typeof data['jw_url'] === 'string' || data['jw_url'] instanceof String)) {
            throw new Error("Expected the field `jw_url` to be a primitive type in the JSON string but got " + data['jw_url']);
        }
        // ensure the json data is a string
        if (data['trailer_url'] && !(typeof data['trailer_url'] === 'string' || data['trailer_url'] instanceof String)) {
            throw new Error("Expected the field `trailer_url` to be a primitive type in the JSON string but got " + data['trailer_url']);
        }
        // ensure the json data is an array
        if (!Array.isArray(data['genres'])) {
            throw new Error("Expected the field `genres` to be an array in the JSON data but got " + data['genres']);
        }
        if (data['countries']) { // data not null
            // ensure the json data is an array
            if (!Array.isArray(data['countries'])) {
                throw new Error("Expected the field `countries` to be an array in the JSON data but got " + data['countries']);
            }
            // validate the optional field `countries` (array)
            for (const item of data['countries']) {
                DirectorFilmsInnerCountriesInner.validateJSON(item);
            };
        }
        if (data['offers']) { // data not null
            // ensure the json data is an array
            if (!Array.isArray(data['offers'])) {
                throw new Error("Expected the field `offers` to be an array in the JSON data but got " + data['offers']);
            }
            // validate the optional field `offers` (array)
            for (const item of data['offers']) {
                DirectorFilmsInnerOffersInner.validateJSON(item);
            };
        }
        if (data['directors']) { // data not null
            // ensure the json data is an array
            if (!Array.isArray(data['directors'])) {
                throw new Error("Expected the field `directors` to be an array in the JSON data but got " + data['directors']);
            }
            // validate the optional field `directors` (array)
            for (const item of data['directors']) {
                DirectorInfo.validateJSON(item);
            };
        }

        return true;
    }


}

Film.RequiredProperties = ["title"];

/**
 * @member {Number} id
 */
Film.prototype['id'] = undefined;

/**
 * @member {String} title
 */
Film.prototype['title'] = undefined;

/**
 * @member {String} description
 */
Film.prototype['description'] = undefined;

/**
 * @member {Number} year
 */
Film.prototype['year'] = undefined;

/**
 * @member {String} rating
 */
Film.prototype['rating'] = undefined;

/**
 * @member {Number} runtime
 */
Film.prototype['runtime'] = undefined;

/**
 * @member {String} lb_url
 */
Film.prototype['lb_url'] = undefined;

/**
 * @member {String} jw_url
 */
Film.prototype['jw_url'] = undefined;

/**
 * @member {String} trailer_url
 */
Film.prototype['trailer_url'] = undefined;

/**
 * @member {Array.<String>} genres
 */
Film.prototype['genres'] = undefined;

/**
 * @member {Array.<module:model/DirectorFilmsInnerCountriesInner>} countries
 */
Film.prototype['countries'] = undefined;

/**
 * @member {Array.<module:model/DirectorFilmsInnerOffersInner>} offers
 */
Film.prototype['offers'] = undefined;

/**
 * @member {Array.<module:model/DirectorInfo>} directors
 */
Film.prototype['directors'] = undefined;






export default Film;

