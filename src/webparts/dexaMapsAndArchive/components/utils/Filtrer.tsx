import "@pnp/sp/items";
import "@pnp/sp/lists";
import "@pnp/sp/webs";
import "@pnp/sp/items/get-all";
import { ActionButton, Checkbox, DefaultButton, Dialog, DialogFooter, DialogType, Dropdown, IDropdownOption, IDropdownStyles, Label, Panel, PrimaryButton, Stack } from 'office-ui-fabric-react';
import * as React from 'react';
import { DISTANCE_END_FILTRAGE, DISTANCE_START_FILTRAGE, sp } from '../../Constants';
import { extendDistanceFiltrer, getLat, getLng } from './utils';

interface IFiltrerProps {
  buttonTitle: string;
  latlng:string;
  dgi:any;
  handleFilter({},{},{}):any;
}

export default function Filtrer (props:IFiltrerProps){
  let [isOpen, setIsOpen] = React.useState(false);
  let [form, setForm] = React.useState({type_de_bien:"Résidentiel", type_de_ref:[], date_de_ref:[], creer_par:null});
  let [typeDeBien, setTypeDeBien] = React.useState("Résidentiel");
  let [alert, setAlert] = React.useState(false);
  let [alertDgi, setAlertDGi] = React.useState(false);
  let [alertAutorisation, setAlertAutorisation] = React.useState(false);
  let lat = getLat(props.latlng);
  let lng = getLng(props.latlng);
  
  const start = {
    latitude: lat,
    longitude: lng
  };
  const dialogContentProps = {
    type: DialogType.normal,
    title: 'Attention',
    subText: "Veuillez remplir tous les champs."
  };
  const dialogContentDGIProps = {
    type: DialogType.normal,
    title: 'Oups',
    subText: "Désolé la zone choisie n'est pas prise en charge par le système."
  };
  const FiltrageDialogContentProps = {
    type: DialogType.largeHeader,
    title: "Oups",
    subText: "Désolé Vous n'êtes pas autorisés d'accéder aux éléments de la liste des références.",
  };
  const modelProps = {
    isBlocking: false,
    styles: { main: { maxWidth: 650 } },
  };
  const dropdownStyles: Partial<IDropdownStyles> = {
    dropdown: { width: 300 },
  };
  const options_type_de_bien: IDropdownOption[] = [
    { key: 'Résidentiel', text: 'Résidentiel'},
    { key: 'Professionnel', text: 'Professionnel'},
    { key: 'Commercial', text: 'Commercial'},
    { key: 'Terrain', text: 'Terrain' },
    { key: 'Villa', text: 'Villa' },
  ];
  const onChange_type_de_bien = (event: React.FormEvent<HTMLDivElement>, item: IDropdownOption): void => {
    setForm({...form, type_de_bien: item.key.toString()});
    setTypeDeBien(item.text);
  };
  const _onChange_type_de_ref = (ev: React.FormEvent<HTMLInputElement>, isChecked: boolean):void => {
    let pos = form.type_de_ref.indexOf(ev.currentTarget.title);
    if(pos === -1 && isChecked){
      form.type_de_ref.push(ev.currentTarget.title);
    }
    if(pos > -1 && !isChecked){
      let removedItem = form.type_de_ref.splice(pos, 1);
    }  
  };
  const _onChange_date_de_ref = (ev: React.FormEvent<HTMLInputElement>, isChecked: boolean):void => {
    let pos = form.date_de_ref.indexOf(ev.currentTarget.title);
    if(pos === -1 && isChecked){
      form.date_de_ref.push(ev.currentTarget.title);
    }
    if(pos > -1 && !isChecked){
      let removedItem = form.date_de_ref.splice(pos, 1);
    } 
  };
  async function _onSubmit(){
    var rest_filterd_list = null;
    if(form.type_de_ref.length===0 || form.date_de_ref.length===0){
      setAlert(true);
    }
    else{
      var time_start = new Date(Date.now());
      var s_start = time_start.getSeconds();
      let A = await sp.web.lists.getByTitle("Pins").items.getAll()
      await sp.web.lists.getByTitle("Pins").items.select("QuiasignalerId", "Nombredesignalement", "validateur_refId", "is_deleted","Id","regionsId","Latitude_Longitude","Date_x0020_de_x0020_la_x0020_r_x","Surface_x0020_pond_x00e9_r_x00e9","Surface_x0020_construite","Surface_x0020_terrain","Type_x0020_de_x0020_bien","Type_x0020_de_x0020_R_x00e9_f_x0", "Title", "Prix_x0020_unitaire_x0020__x002F","Prix_x0020_unitaire_x0020_pond_x","Prix_x0020_unitaire_x0020_terrai","Localis_x00e9_")
      .getAll().then(async res=>{
        console.log("Res avant filter", res)
        rest_filterd_list = extendDistanceFiltrer(res,start,DISTANCE_START_FILTRAGE, DISTANCE_END_FILTRAGE, form.type_de_bien, form.type_de_ref, form.date_de_ref);
        props.handleFilter(rest_filterd_list.filterd_list_dexa, rest_filterd_list.dis,typeDeBien);
      }).catch(error=>{
        if(error.status === 404 || (error.response.status && error.response.status === 404)){
          setAlertAutorisation(true);
        }
      });
      setIsOpen(false);
    }
  }
  return (
    <div>
      {alert?       
        <Dialog hidden={!alert} onDismiss={()=>setAlert(false)} dialogContentProps={dialogContentProps} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlert(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
      :<></>}
      {alertDgi?       
        <Dialog hidden={!alertDgi} onDismiss={()=>setAlertDGi(false)} dialogContentProps={dialogContentDGIProps} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlertDGi(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
      :<></>}      
      {alertAutorisation?       
        <Dialog hidden={!alertAutorisation} onDismiss={()=>setAlertAutorisation(false)} dialogContentProps={FiltrageDialogContentProps} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlertAutorisation(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
      :<></>}
      <Stack horizontal horizontalAlign="start">
        <ActionButton iconProps={{iconName: 'Financial'}} text={props.buttonTitle} onClick={() => setIsOpen(true)}/>
      </Stack>
      <Panel isOpen={isOpen} onDismiss={()=> setIsOpen(false)} headerText="FILTRAGE" closeButtonAriaLabel="Close">
        <Stack tokens={{childrenGap:10}}>{/* stack organise les flex */}
          <Dropdown placeholder="Selectionner le type de bien" label="TYPE DE BIEN" options={options_type_de_bien} styles={dropdownStyles} defaultSelectedKey={form.type_de_bien} onChange={onChange_type_de_bien}/>
          <Stack tokens={{ childrenGap: 10}}>
            <Label>TYPE DE RÉFÉRENCE</Label>
            <Stack horizontal horizontalAlign="start" tokens={{childrenGap:65}}>
              <Checkbox  value={1} title="Vente" label="Vente" onChange={_onChange_type_de_ref } />
              <Checkbox value={2} title="Location" label="Location" onChange={_onChange_type_de_ref } />
            </Stack>
          </Stack>
          <Stack tokens={{ childrenGap: 10}}>
            <Label>DATE DE RÉFÉRENCE</Label>
            <Stack horizontal horizontalAlign="start" tokens={{childrenGap:65}}>
              <Checkbox  value={2021} title="2021" label="2021" onChange={_onChange_date_de_ref } />
              <Checkbox value={2022} title="2022" label="2022" onChange={_onChange_date_de_ref } />
            </Stack>
          </Stack>
          <Stack horizontal horizontalAlign="end" tokens={{childrenGap:30}}>
            <PrimaryButton text="Filtrer" onClick={async() => {await _onSubmit(); setIsOpen(false)}}></PrimaryButton>
            <DefaultButton text="Cancel" onClick={() => setIsOpen(false)}></DefaultButton>
          </Stack>
        </Stack>
      </Panel>
    </div>
  );
}
