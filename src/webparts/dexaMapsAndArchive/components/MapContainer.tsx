import "@pnp/sp/clientside-pages/web";
import "@pnp/sp/webs";
import "@pnp/sp/items/get-all";
import GoogleMapReact from 'google-map-react';
import { ActionButton, Dialog, DialogType, Stack } from 'office-ui-fabric-react';
import * as React from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { sp, urlAddRef, urlPropertieRef } from '../Constants';
import { getLat, getLng, isPointInPolygon, WindowPopUp } from './utils/utils';
import Evaluer from './utils/Evaluer';
import Filtrer from './utils/Filtrer';
import FiltrerRapport from './utils/FiltrerRapport';
import FiltrerWithUser from "./utils/FiltrerWithUser";
import styles from './DexaMapsAndArchive.module.scss';
import PopOutFilter from './fabric-ui/PopOutFilter';
import ValiderRef from "./utils/ValiderRef";
import EditerRef from "./utils/EditerRef";
import SuppRef from "./utils/SuppRef";
import SignalerRef from "./utils/SignRef";

interface IMapContainerProps {
  GoogleKey:string;
  context:any;
}

export default function MapContainer(props:IMapContainerProps){
  let [updatedMarker, setUpdatedMarker]= React.useState(false);
  let [rightClickMarker, setRightClickMarker]= React.useState(false);
  let [rightClickMap, setRightClickMap]= React.useState(false);
  let [copySuccess, setCopySuccess]= React.useState('');
  let [lat, setLat]= React.useState(null);
  let [lng, setLng]= React.useState(null);
  let [maps, setMaps]= React.useState(null);
  let [map, setMap]= React.useState(null);
  let [result, SetResult]= React.useState(null);
  let [popupInfo, setPopupInfo]= React.useState(null);
  let [popupInfoRapport, setPopupInfoRapport]= React.useState(null);
  let [DGI, setDGI] = React.useState(null);
  let [popOut, setPopOut] = React.useState(false);
  let [information, setInformation] = React.useState(null);
  let [typeDeBien, setTypeDeBien] = React.useState("");
  let [rapportClassicMarkers, setRapportClassicMarkers]= React.useState(null);
  let [grandRapportMarkers, setGrandRapportMarkers]= React.useState(null);
  let [dexa_markers, setDexa_markers]= React.useState(null);
  let [isValidateur, setIsValidateur]= React.useState(null);
  let [isNotValid, setIsNotValid]= React.useState(null);
  let [windowPopUp, setWindowPopUp]= React.useState(null);
  let [isNotSignaler, setIsNotSignaler]= React.useState(null);
  let [isSignaler, setIsSignaler]=React.useState(null);

  ///////////////////////////////////////////////////////////////////////////////////////////////////
  const FiltrageDialogContentProps = {
    type: DialogType.largeHeader,
    title: "Analyse de la zone",
    subText: ''
  };
  const modelProps = {
    isBlocking: false,
    styles: { main: { maxWidth: 650 } },
  };
  const defaultProps = {
    center: {
      lat: 33.53681110956971,
      lng: -7.529033709989725
    },
    zoom: 11,
    disableDefaultUI: false,
  };
  const handleApiLoaded = (map, maps) => {
    setMaps(maps);
    setMap(map);
    maps.event.addListener(map, "rightclick", async function(event) {
      maps.event.trigger(map, 'resize'); 
      setTimeout(()=> {
        setCopySuccess('Copied');
        setPopupInfo(null);
        setRightClickMarker(rightClickMarker => {
          if(rightClickMarker){
            event.preventDefault;
            setRightClickMarker(false);
          }
          else{
            setRightClickMap(true);
            setPopupInfo(null);
            var _lat = parseFloat(event.latLng.lat());
            var _lng = parseFloat(event.latLng.lng());
            setLat(_lat);
            setLng(_lng);
            navigator.clipboard.writeText(event.latLng.lat()+","+event.latLng.lng());
            getDGI(_lat,_lng);
          }
          return rightClickMarker;
        });
      }, 200);
    });
  };
  const Marker = ({ marker, lat, lng, text}) => {
    if(marker.Localis_x00e9_=="Oui" && marker.Type_x0020_de_x0020_R_x00e9_f_x0 === "Vente")
      return <div className={ styles.markerVenteLocaliser }
      onClick={()=> {onMarkerClick(marker);}}
      onContextMenu={()=> onMarkerRightClick(marker)}></div>
    else if(marker.Localis_x00e9_=="Non" && marker.Type_x0020_de_x0020_R_x00e9_f_x0 === "Vente")
      return <div className={ styles.markerVenteNonLocaliser }
      onClick={()=> {onMarkerClick(marker);}}
      onContextMenu={()=> onMarkerRightClick(marker)}></div>
    else if(marker.Localis_x00e9_=="Oui" && marker.Type_x0020_de_x0020_R_x00e9_f_x0 === "Location")
      return <div className={ styles.markerLocationLocaliser }
      onClick={()=> {onMarkerClick(marker);}}
      onContextMenu={()=> onMarkerRightClick(marker)}></div>
    else if(marker.Localis_x00e9_=="Non" && marker.Type_x0020_de_x0020_R_x00e9_f_x0 === "Location")
      return <div className={ styles.markerLocationNonLocaliser }
      onClick={()=> {onMarkerClick(marker);}}
      onContextMenu={()=> onMarkerRightClick(marker)}></div>
  };
  const MarkerRapportClassic = ({ marker, lat, lng, text}) => {
    return <div className={ styles.markerRapportClassic }
      onClick={()=> {onMarkerRapportClick(marker);}}
      onContextMenu={()=> onMarkerRightClick(marker)}>
    </div>
  };
  const MarkerGrandProjet = ({ marker, lat, lng, text}) => {
    return <div className={ styles.markerGrandProjet }
      onClick={()=> {onMarkerRapportClick(marker);}}
      onContextMenu={()=> onMarkerRightClick(marker)}>
    </div>
  };
  const Popup = ({ lat, lng}) => {
    return  (<div className={styles.popupMarker}>
        <div className={styles.CloseDiv} onClick={()=> setPopupInfo(false)}>X</div>
        <div className={styles.arrowPopUp}></div>
        <div><span className={styles.spanInfo}>Type de bien:</span><span>{popupInfo.Type_x0020_de_x0020_bien}</span></div>
        {popupInfo.Surface_x0020_terrain?<div><span className={styles.spanInfo}>Surface Terrain:</span><span>{popupInfo.Surface_x0020_terrain} m²</span></div>:<></>}
        {popupInfo.Surface_x0020_construite?<div><span className={styles.spanInfo}>Surface Construite:</span><span>{popupInfo.Surface_x0020_construite} m²</span></div>:<></>}
        {popupInfo.Surface_x0020_pond_x00e9_r_x00e9?<div><span className={styles.spanInfo}>Surface Pondéré:</span><span>{popupInfo.Surface_x0020_pond_x00e9_r_x00e9} m²</span></div>:<></>}
        <br/>
        {/* {!popupInfo.validateur_refId?<ValiderRef idRef={popupInfo.Id} buttonTitle="Valider la référence" ctx={props.context}></ValiderRef>:<></>} */}
        {!popupInfo.validateur_refId?<EditerRef  idRef={popupInfo.Id} buttonTitle="Editer la référence" ctx={props.context} ></EditerRef>:<></>}
        {!popupInfo.validateur_refId?<SuppRef idRef ={popupInfo.Id} buttonTitle="Supprimer la référence" ctx={props.context}></SuppRef>:<></>}
      <SignalerRef idRef ={popupInfo.Id} buttonTitle="Signaler la référence" ctx={props.context} user={popupInfo.QuiasignalerId} nbrSignals={popupInfo.Nombredesignalement} ></SignalerRef>
        <a className={styles.rightFloat} href="#" onClick={(event)=> {
          event.preventDefault(); 
          setWindowPopUp(WindowPopUp('', urlPropertieRef+popupInfo.Id, 'Pins'));
        }}>Voir plus...</a>
      </div>);
  };
  const PopupRapport = ({ lat, lng}) => {
    return <div className={styles.popupMarker}>
      <div className={styles.CloseDiv} onClick={()=> setPopupInfoRapport(false)}>X</div>
      <div className={styles.arrowPopUp}></div>
      <span className={styles.spanInfo}>Type de bien: </span>{popupInfoRapport.Type_x0020_de_x0020_bien}<br/>
      {popupInfoRapport.Surface_x0020_pond_x00e9_r_x00e9?<><span className={styles.spanInfo}>Surface pondéré: </span>{popupInfoRapport.Surface_x0020_pond_x00e9_r_x00e9} Dhs/m2<br/></>:<></>}
      {popupInfoRapport.Surface_x0020_construite?<><span className={styles.spanInfo}>Surface construite: </span>{popupInfoRapport.Surface_x0020_construite} Dhs/m2<br/></>:<></>}
      {popupInfoRapport.Surface_x0020_terrain?<><span className={styles.spanInfo}>Surface terrain: </span>{popupInfoRapport.Surface_x0020_terrain} Dhs/m2<br/></>:<></>}
      <span className={styles.spanInfo}>Prix total de l'expertise: </span>{popupInfoRapport.Prix_x0020_total_x0020_de_x0020_} Dhs
      </div>
  };
  const PopupRightOrganisme = ({ lat, lng , modaleTitle}) => {
    return <div className={styles.popupRight}>
      <div className={styles.CloseDiv} onClick={()=> setRightClickMap(false)}>X</div>
      <div className={styles.arrowPopUp}></div>
      <br/>
      <div>
        <CopyToClipboard text={lat+","+lng} onCopy={() => {setCopySuccess('Copied!');}} className={styles.Pointer}>
          <span>{parseFloat(lat).toFixed(5)},{parseFloat(lng).toFixed(5)}</span>
        </CopyToClipboard>
        <span className={styles.CopyToClipboardMsg}>&nbsp;{copySuccess}</span>
      </div>
      <Filtrer dgi={DGI}  buttonTitle="Analyser la zone" latlng={lat+","+lng} handleFilter={ async (items_dexa,distance,type_de_bien) => await displayMarker(items_dexa,distance,type_de_bien)} ></Filtrer>
      <FiltrerRapport dgi={DGI} buttonTitle="Afficher les rapports" latlng={lat+","+lng} handleFiltrerRapport={ async (rapport_classic,grand_rapport) => await displayRapport(rapport_classic,grand_rapport)} ></FiltrerRapport>
      <Evaluer dgi={DGI} buttonTitle="Evaluer le bien" latlng={lat+","+lng} handleEvaluer={(result) => {if(result!=null) {moreInfo(result);}}} ></Evaluer>
      {/*<DialogEvaluation/>
      <br/>*/}
      <ActionButton iconProps={{iconName: 'Add'}} text="Ajouter une référence" onClick={(event)=> {event.preventDefault(); WindowPopUp('', urlAddRef, "");}}/>
      <FiltrerWithUser context={props.context} handleFilterWhithUser={async (items_dexa) => await displayAllMarker(items_dexa)} buttonTitle={"Fitrage par user"} latlng={lat+","+lng} dgi={DGI}/>
    </div>;
  };
  const SearchBox = ({ map, maps, onPlacesChanged, placeholder }) => {
    let input = React.useRef(null);
    const searchBox = React.useRef(null);
    React.useEffect(() => {
      if (!searchBox.current && maps && map) {
        searchBox.current = new maps.places.SearchBox(input.current);
        maps.event.addListener(searchBox.current, 'places_changed', function() {
          var places = searchBox.current.getPlaces();
          places.forEach(place => {
            var myLatlng = new maps.LatLng(place.geometry.location.lat(),place.geometry.location.lng());
            map.setCenter(myLatlng);
            var marker = new maps.Marker({
              position: myLatlng,
              map:map
            });
          });
        });
      }
      return () => {
        if (maps) {
          searchBox.current = null;
          maps.event.clearInstanceListeners(searchBox);
        }
      };
    });
    let inputSearch = <div key={"inputSearch"}><input ref={input} placeholder={placeholder} className={styles.googleMapSearchBox} type="text" /></div>;
    return inputSearch;
  };
  ///////////////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////
    /*async function getIfSign(){
     var query = function(element) {
       return element.ID === popupInfo.ID;
     };
     var compar = await sp.web.lists.getByTitle("Pins").items.getAll();
    var compara = await compar.filter(query)
     if(compara[0].QuiasignalerId === null)
     setIsNotSignaler(compara);
     else
     setIsNotSignaler(null)
   }*/
   
  ////////
  
  async function getDGI(lat,lng){
    var query = function(element) {
      return isPointInPolygon(lat, lng, element.Polygone);
    };
    await sp.web.lists.getByTitle("l_ref_DGI").items.getAll().then(res=>{
    const dgi = res.filter(query);
    setDGI(dgi);
    });
  }
  async function onMarkerClick(marker) {
    setPopupInfo(null);
    setPopupInfoRapport(null);
    setRightClickMap(false);
    setPopupInfo(marker);
  }
  async function onMarkerRapportClick(marker) {
    setPopupInfo(null);
    setPopupInfoRapport(null);
    setRightClickMap(false);
    setPopupInfoRapport(marker);
  }
  async function onMarkerRightClick(marker) {
    setPopupInfo(null);
    setRightClickMarker(rightClickMarker=> {return true;});
    return rightClickMarker;
  }
  function moreInfo(evaluation){
    SetResult(evaluation);
  }
  async function displayMarker (item_dexa:any, distance:any, type_de_bien:any) {
    setPopupInfo(null);
    setPopupInfoRapport(null);
    setTypeDeBien(type_de_bien);
    setRapportClassicMarkers(null);
    await setDexa_markers(item_dexa);
    setUpdatedMarker(true);
    var result = {
      dgi_zone:DGI,
      ref_dexa: item_dexa,
      distance: distance,
      type_de_bien: type_de_bien,
    };
    setInformation(result);
    setPopOut(true);
  }
  async function displayAllMarker (item_dexa:any) {
    setRapportClassicMarkers(null);
    await setDexa_markers(item_dexa);
    setUpdatedMarker(true);
    var result = {
      ref_dexa: item_dexa
    };
    setInformation(result);
  }
  async function displayRapport (rapport_classic:any, grand_rapport:any) {
    setPopupInfo(null);
    setPopupInfoRapport(null);
    setDexa_markers(null)
    await setRapportClassicMarkers(rapport_classic);
    await setGrandRapportMarkers(grand_rapport);
    setUpdatedMarker(true);
  }

  return (
    <div className={styles.googleMapReact}>
      {popOut?
        <Dialog hidden={!popOut} onDismiss={()=> setPopOut(false)} dialogContentProps={FiltrageDialogContentProps} modalProps={modelProps} styles={{main: {selectors: {['@media (min-width: 480px)']: {width: 550, height: 555, minWidth: 450, maxWidth: '1000px'}}}}}>
          <PopOutFilter Information={information}/>
        </Dialog>
      :<></>}
      <Stack horizontal>
        <div> 
          <SearchBox onPlacesChanged={null} map={map} maps={maps} placeholder={"Search location ..."}/>
        </div>
      </Stack>
      <GoogleMapReact bootstrapURLKeys={{ key: props.GoogleKey, libraries:['places'] }} defaultCenter={defaultProps.center} defaultZoom={defaultProps.zoom} yesIWantToUseGoogleMapApiInternals onGoogleApiLoaded={({ map, maps }) => handleApiLoaded(map, maps)} options={map => ({streetViewControl: true, mapTypeControl: true, mapTypeControlOptions: {style: map.MapTypeControlStyle.DEFAULT, position: map.ControlPosition.TOP_RIGHT, mapTypeIds: [map.MapTypeId.ROADMAP, map.MapTypeId.SATELLITE, map.MapTypeId.HYBRID]}})}>
        {rapportClassicMarkers ? rapportClassicMarkers.map(marker=> <MarkerRapportClassic lat={getLat(marker.Latitude_Longitude)} lng={getLng(marker.Latitude_Longitude)} text={marker.Title} marker={marker}/>):<></>}
        {grandRapportMarkers ? grandRapportMarkers.map(marker=> <MarkerGrandProjet lat={getLat(marker.Latitude_Longitude)} lng={getLng(marker.Latitude_Longitude)} text={marker.Title} marker={marker}/>):<></>}
        {updatedMarker&&dexa_markers ? dexa_markers.map(marker=> <Marker lat={getLat(marker.Latitude_Longitude)} lng={getLng(marker.Latitude_Longitude)} text={marker.Title} marker={marker}/>):<></>}
        {popupInfoRapport ? <PopupRapport lat={getLat(popupInfoRapport.Latitude_Longitude)} lng={getLng(popupInfoRapport.Latitude_Longitude)}/>:<></>}
        {popupInfo ? <Popup lat={getLat(popupInfo.Latitude_Longitude)} lng={getLng(popupInfo.Latitude_Longitude)}/>:<></>}
        {rightClickMap ? <PopupRightOrganisme lat={lat} lng={lng} modaleTitle={"Ajouter Réference"}/>:<></>}
      </GoogleMapReact>
    </div>
  );
}
