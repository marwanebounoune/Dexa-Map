import { spfi, SPBrowser   } from "@pnp/sp";

export const sp = spfi().using(SPBrowser({ baseUrl: "https://agroupma.sharepoint.com/sites/DEXA2022/" }));

export const MAX_SCORE:number = 5;
export const MIN_SCORE:number = 1;
export const RATIO:number = 15/100;
export const SURFACE_COEFFICIENT:number = 1;
export const SITUATION_GENERAL_COEFFICIENT:number = 2;
export const STANDING_APPARTEMENT_COEFFICIENT:number = 1;
export const STANDING_IMMEUBLE_COEFFICIENT:number =1;
export const DISTANCE_START_FILTRAGE:number = 1000;//1km
export const DISTANCE_END_FILTRAGE:number = 3000;//1km
export const DISTANCE_START_EVALUATION:number = 250;//250m
export const DISTANCE_END_EVALUATION:number = 750;//750m
export const DGI_COEFFICIENT_FILTER:number = 0.35;
export const reducer = (previousValue, currentValue) => previousValue + currentValue;
export const urlAddRef = "https://agroupma.sharepoint.com/sites/DEXA2022/_layouts/15/listform.aspx?PageType=8&ListId=%7B91F90891-34B7-4F13-9A6C-6C3B797EEDFD%7D&RootFolder=%2Fsites%2FDEXA2022%2FLists%2FPins&Source=https%3A%2F%2Fagroupma.sharepoint.com%2Fsites%2FDEXA2022%2FLists%2FPins%2FAllItems.aspx&ContentTypeId=0x0100372FFDC88828B0479A9E40A2618E7968"
export const urlPropertieRef = "https://agroupma.sharepoint.com/sites/DEXA2022/Lists/Pins/DispForm.aspx?ID="