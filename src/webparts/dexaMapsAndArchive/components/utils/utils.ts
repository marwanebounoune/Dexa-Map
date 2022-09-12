import "@pnp/sp/webs";
import "@pnp/sp/items/get-all";
import * as turf from "@turf/turf";
import * as haversine from "haversine";
import { DGI_COEFFICIENT_FILTER, MAX_SCORE, MIN_SCORE, RATIO, reducer, SITUATION_GENERAL_COEFFICIENT, STANDING_APPARTEMENT_COEFFICIENT, STANDING_IMMEUBLE_COEFFICIENT, SURFACE_COEFFICIENT, sp } from "../../Constants";


export function isPointInPolygon(lat:number, lng:number, poly:any ){
    var point = turf.point([lng, lat]);
    return turf.booleanPointInPolygon(point, turf.polygon(JSON.parse(poly)));
}
export function getLat(latlng:string){
    var lat = latlng.split(",",1)[0];
    return parseFloat(lat);
}
export function getLng(latlng:string){
    var lng = latlng.split(",",2)[1];
    return parseFloat(lng);
}
export async function getUser(email: string) {
    let user = await sp.web.ensureUser(email);
    return user;
}
export async function WindowPopUp(modalTitle:string, url:string, from_list:string){
    var left = (screen.width/2)-(840/2);
    var top = (screen.height/2)-(600/2);
    var url_page = url;
    var credit = null;
    const currentUser = await sp.web.currentUser();
    var userId =  currentUser.Id;
    if(from_list === "Pins"){
        const credits = await sp.web.lists.getByTitle("l_credits").items.getAll();
        var query = function(element) {
            return element.userId === userId;
        };
        credit = credits.filter(query);
        var email: string = currentUser.Email.toString();
        if (email != "alami.saad@agroup.ma" && email != "valactif.deev@agroup.ma" && email != "alami.mohamed@agroup.ma" && (credit.length===0 || credit[0].Cr_x00e9_dit_x0020_journalier === 0 || credit[0].Cr_x00e9_dit_x0020_mensuel == 0)){
            url_page = "https://agroupma.sharepoint.com/:u:/s/DEXA2022/EeHkEXWh9lNKr_t2npJ5SJEBIRBL6OhvBn6BKfxB8CFcNA?e=7bfopv";
        }
        else{
            if(email != "alami.saad@agroup.ma" && email != "valactif.deev@agroup.ma" && email != "alami.mohamed@agroup.ma" && credit){
                await sp.web.lists.getByTitle("l_credits").items.getById(credit[0].Id).update({
                    Cr_x00e9_dit_x0020_journalier: credit[0].Cr_x00e9_dit_x0020_journalier-1,
                    Cr_x00e9_dit_x0020_mensuel: credit[0].Cr_x00e9_dit_x0020_mensuel-1
                });
            }
        }
    }
    window.open(url_page, modalTitle, "width=840,height=600,menubar=no,toolbar=no,directories=no,titlebar=no,resizable=no,scrollbars=no,status=no,location=no,top="+top+", left="+left);
}
export function estimated_price(Max_price:number, Min_price:number, calculated_score:number){
    var _calculated_A_coefficient =calculated_A_coefficient(Max_price,Min_price);
    var _calculated_B_coefficient = calculated_B_coefficient(Max_price, Min_price);
    return _calculated_A_coefficient*calculated_score+ _calculated_B_coefficient;
}
export function calculated_A_coefficient(Max_price:number, Min_price:number){
    return (Max_price-Min_price + 2 * RATIO)/(MAX_SCORE-MIN_SCORE);
}
export function calculated_B_coefficient(Max_price:number, Min_price:number){
    return Min_price - RATIO - calculated_A_coefficient(Max_price, Min_price);
}
export function somme_score(){
    return SURFACE_COEFFICIENT + SITUATION_GENERAL_COEFFICIENT + STANDING_APPARTEMENT_COEFFICIENT + STANDING_IMMEUBLE_COEFFICIENT;
}
export function calculated_score(surface_score:number, situation_general_score:number, standing_appt_score:number, standing_immeuble_score:number ){
    return ((surface_score * SURFACE_COEFFICIENT + situation_general_score * SITUATION_GENERAL_COEFFICIENT +  standing_appt_score * STANDING_APPARTEMENT_COEFFICIENT +  standing_immeuble_score * STANDING_IMMEUBLE_COEFFICIENT) / somme_score());
}
export function is_valide_PU(prix_dgi:number, prix_ref:number){
    if(prix_ref >= prix_dgi - prix_dgi*DGI_COEFFICIENT_FILTER && prix_ref <= prix_dgi + prix_dgi*DGI_COEFFICIENT_FILTER ){
        return true;
    }
    return false;
}
export function extendDistanceEvaluer(itemsDexa:any, start_point:any, start_dis:number, end_dis:number, DGI:any, type_de_bien:string){
    var array_prix_dexa:any = [];
    var query = function(element) {
        var lat = getLat(element.Latitude_Longitude);
        var lng = getLng(element.Latitude_Longitude);
        var end_point = {
            latitude: lat,
            longitude: lng
        };
        var dis = haversine(start_point, end_point);
        var type_de_bien = element.Type_x0020_de_x0020_bien;
        var el_prix:number = null;
        if(type_de_bien === "Résidentiel" || type_de_bien === "Commercial" || type_de_bien === "Professionnel")
            el_prix = parseInt(element.Prix_x0020_unitaire_x0020_pond_x);
        else
            el_prix = parseInt(element.Prix_x0020_unitaire_x0020_terrai);
        var _is_valide_PU = is_valide_PU(parseInt(DGI.Prix_unitaire),el_prix);
        var el =  element.Type_x0020_de_x0020_bien === type_de_bien && element.Type_x0020_de_x0020_R_x00e9_f_x0 === "Vente" && dis <= start_dis/1000 && _is_valide_PU;
        if (el){
            array_prix_dexa.push(el_prix);
            return el;
        }
    };
    const filterd_list_dexa = itemsDexa.filter(query);
    if (start_dis === end_dis || filterd_list_dexa.length > 3){
        return {filterd_list:filterd_list_dexa, dis:start_dis, nbr_dexa:filterd_list_dexa.length, array_prix_dexa:array_prix_dexa} ;
    }
    return extendDistanceEvaluer(itemsDexa,start_point, start_dis+100, end_dis,DGI, type_de_bien);
}
export function extendDistanceFiltrer(itemsDexa:any, start_point:any, start_dis:number, end_dis:number, type_de_bien:string,type_de_ref:string[], date_de_ref:string[]){
    if (type_de_bien === "Villa")
        var query = function(element) {
            var lat = getLat(element.Latitude_Longitude);
            var lng = getLng(element.Latitude_Longitude);
            var end_point = {
                latitude: lat,
                longitude: lng
            };
            var dis = haversine(start_point, end_point);
            var date = new Date(element.Date_x0020_de_x0020_la_x0020_r_x).getFullYear().toString()
            return element.is_deleted ==="Non" && (element.Type_x0020_de_x0020_bien === "Villa" || element.Type_x0020_de_x0020_bien === "Terrain Villa") && type_de_ref.indexOf(element.Type_x0020_de_x0020_R_x00e9_f_x0)!=-1 && date_de_ref.indexOf(date)!=-1 && dis <= start_dis/1000;
        };
    else if (type_de_bien === "Terrain")
        var query = function(element) {
            var lat = getLat(element.Latitude_Longitude);
            var lng = getLng(element.Latitude_Longitude);
            var end_point = {
                latitude: lat,
                longitude: lng
            };
            var dis = haversine(start_point, end_point);
            var date = new Date(element.Date_x0020_de_x0020_la_x0020_r_x).getFullYear().toString()
            console.log("Type de bien: ", element.Type_x0020_de_x0020_bien)
            return element.is_deleted ==="Non" && (element.Type_x0020_de_x0020_bien === "Terrain Agricole" || element.Type_x0020_de_x0020_bien === "Terrain Construit" || element.Type_x0020_de_x0020_bien === "Terrain Urbain" || element.Type_x0020_de_x0020_bien === "Terrain Villa") && type_de_ref.indexOf(element.Type_x0020_de_x0020_R_x00e9_f_x0)!=-1 && date_de_ref.indexOf(date)!=-1 && dis <= start_dis/1000;
        };
    else
        var query = function(element) {
            var lat = getLat(element.Latitude_Longitude);
            var lng = getLng(element.Latitude_Longitude);
            var end_point = {
                latitude: lat,
                longitude: lng
            };
            var dis = haversine(start_point, end_point);
            var date = new Date(element.Date_x0020_de_x0020_la_x0020_r_x).getFullYear().toString()
            return element.is_deleted ==="Non" && element.Type_x0020_de_x0020_bien === type_de_bien && type_de_ref.indexOf(element.Type_x0020_de_x0020_R_x00e9_f_x0)!=-1 && date_de_ref.indexOf(date)!=-1 && dis <= start_dis/1000;

        };
    const filterd_list_dexa = itemsDexa.filter(query);
    if (start_dis === end_dis || filterd_list_dexa.length > 10){
        return {
            dis:start_dis/1000,
            filterd_list_dexa:filterd_list_dexa,
        };
    }
    return extendDistanceFiltrer(itemsDexa,start_point, start_dis+250, end_dis, type_de_bien, type_de_ref, date_de_ref);//pas 250 m
}
export function extendDistanceFiltrerWithUser(itemsDexa:any, start_point:any, start_dis:number, end_dis:number){
    var query = function(element) {
        var lat = getLat(element.Latitude_Longitude);
        var lng = getLng(element.Latitude_Longitude);
        var end_point = {
            latitude: lat,
            longitude: lng
        };
        var dis = haversine(start_point, end_point);
        return element.is_deleted ==="Non" && dis <= start_dis/1000;
    };
    
    const filterd_list_dexa = itemsDexa.filter(query);
    if (start_dis === end_dis || filterd_list_dexa.length > 10){
        return filterd_list_dexa;
    }
    return extendDistanceFiltrerWithUser(itemsDexa,start_point, start_dis+250, end_dis);
}
export function extendDistanceFiltrerRapport(rapport_classic:any,grand_rapport:any,start_point:any, start_dis:number, end_dis:number,type_de_bien:string[]){
    var query = function(element) {
        var isIncluded = false;
        if(element.Latitude_Longitude){
            var lat = getLat(element.Latitude_Longitude);
            var lng = getLng(element.Latitude_Longitude);
            var end_point = {
                latitude: lat,
                longitude: lng
            };
            var dis = haversine(start_point, end_point);
            var element_type_de_bien = element.Type_x0020_de_x0020_bien;
            if(element_type_de_bien!=null){
                isIncluded =  type_de_bien.some(value => element_type_de_bien.includes(value));
            }
            if(type_de_bien.length===0){
                return element.FileSystemObjectType === 0 && dis <= start_dis/1000;
            }
            else{
                return isIncluded && element.FileSystemObjectType === 0 && dis <= start_dis/1000;
            }
        }
    };
    const filterd_list_rapport_classic = rapport_classic.filter(query);
    const filterd_list_grand_rapport = grand_rapport.filter(query);
    if (start_dis === end_dis || (filterd_list_rapport_classic.length+filterd_list_grand_rapport.length) > 10){
        return {
            dis:start_dis/1000,
            filterd_list_rapport_classic:filterd_list_rapport_classic,
            filterd_list_grand_rapport:filterd_list_grand_rapport
        };
    }
    return extendDistanceFiltrerRapport(rapport_classic, grand_rapport,start_point, start_dis+250, end_dis, type_de_bien);//pas 250 m
}
export async function get_dgi_zone(lat:number, lng:number) {
    await sp.web.lists.getByTitle("l_ref_DGI").items.getAll().then(res=>{
        var query = function(element) {
            return isPointInPolygon(lat, lng, element.Polygone);
        };
        const dgi = res.filter(query);
        return dgi;
    });
}
export function Mediane(arr:any){
    if(arr.length != 0){
        arr.sort(function(a, b){ return a - b; });//sort array
        var i = arr.length / 2;//find median index
        return i % 1 == 0 ? Math.floor((arr[i - 1] + arr[i]) / 2) : Math.floor(arr[Math.floor(i)]); // math floor retourne Un nombre qui représente le plus grand entier inférieur ou égal à la valeur passée en argument.
    }
    else{
        return 0;
    }
}
export function EcartType(arr:any){
    if(arr.length!=0){
        var sum = arr.reduce(reducer);
        var n = arr.length;
        var mean = sum / n;
        var stdev:number = Math.sqrt((Math.pow(sum,2) / n) - (Math.pow(mean,2)));
        return Math.floor(stdev);
    }
    else{
        return 0;
    }
}
export function Prix_unitaire_moyen(array:any){
    if(array.length != 0){
        let _prix_moyen = array.reduce(reducer)/array.length;
        return Math.floor(_prix_moyen);
    }
    return 0;
}
export function Prix_unitaire_max(array:any){
    if(array.length != 0){
        return Math.max.apply(null, array);
    }
    return 0;
}
export function Prix_unitaire_min(array:any){
    if(array.length != 0){
        return Math.min.apply(null, array);
    }
    return 0;
}
export function getAbsoluteRapportUrl(EncodedAbsUrl:string, FileLeafRef:string){
    var pathUrl:any = EncodedAbsUrl.split(encodeURIComponent(FileLeafRef));
    return pathUrl[0];
}
export function numStr(a, b) {
    a = '' + a;
    b = b || ' ';
    var c = '',
        d = 0;
    while (a.match(/^0[0-9]/)) {
      a = a.substr(1);
    }
    for (var i = a.length-1; i >= 0; i--) {
      c = (d != 0 && d % 3 == 0) ? a[i] + b + c : a[i] + c;
      d++;
    }
    return c;
}


