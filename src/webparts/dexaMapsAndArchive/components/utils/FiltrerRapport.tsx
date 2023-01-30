import "@pnp/sp/webs";
import "@pnp/sp/lists/web";
import "@pnp/sp/fields";
import "@pnp/sp/items";
import "@pnp/sp/items/get-all";
import { ActionButton, Checkbox, DefaultButton, Dialog, DialogFooter, DialogType, Dropdown, IDropdownOption, IDropdownStyles, Label, Panel, PrimaryButton, Stack } from 'office-ui-fabric-react';
import * as React from 'react';
import { DISTANCE_END_FILTRAGE, DISTANCE_START_FILTRAGE, sp } from '../../Constants';
import { extendDistanceFiltrerRapport, getLat, getLng } from './utils';
import * as haversine from "haversine";

interface IFiltrerRapportProps {
  buttonTitle: string;
  latlng:string;
  dgi:any;
  handleFiltrerRapport({},{}):any;
}

export default function FiltrerRapport (props:IFiltrerRapportProps){
  let [isOpen, setIsOpen] = React.useState(false);
  let [submitClick, setSubmitClick] = React.useState(false);
  let [form, setForm] = React.useState({type_de_bien:[], type_rapport:[], annees:[]});
  let [alertAutorisation, setAlertAutorisation] = React.useState(false);
  let [alertDgi, setAlertDGi] = React.useState(false);
  let lat = getLat(props.latlng);
  let lng = getLng(props.latlng);
  let [currentYear, setCurrentYear] = React.useState(Date);
  let [alertTous, setAlertTous] = React.useState(false);
  const arch = "Archive ";

  const start = {
    latitude: lat,
    longitude: lng
  };
  const dialogContentDGIProps = {
    type: DialogType.normal,
    title: 'Oups',
    subText: 'Désolé la zone choisie n\'est pas prise en charge par le système.',
  };
  const dialogContentPropsTous = {
    type: DialogType.normal,
    title: 'Attention',
    subText: "Veuillez deselectionner le champ 'Tous'."
  };
  const FiltrageDialogContentProps = {
    type: DialogType.largeHeader,
    title: "Analyse de la zone",
    subText: '',
  };
  const modelProps = {
    isBlocking: false,
    styles: { main: { maxWidth: 650 } },
  };
  const dropdownStyles: Partial<IDropdownStyles> = {
    dropdown: { width: 300 },
  };
  const options_type_de_bien: IDropdownOption[] = [
    { key: 'Assiette foncière', text: 'Assiette foncière' },
    { key: 'Avancement des travaux', text: 'Avancement des travaux' },
    { key: 'Clinique', text: 'Clinique' },
    { key: 'Commercial', text: 'Commercial' },
    { key: 'Duplex', text: 'Duplex' },
    { key: 'FDC', text: 'FDC' },
    { key: 'Hangars', text: 'Hangars' },
    { key: 'Immeuble', text: 'Immeuble' },
    { key: 'Local commercial', text: 'Local commercial' },
    { key: 'Maison', text: 'Maison' },
    { key: 'Matériel', text: 'Matériel' },
    { key: 'Professionnel', text: 'Professionnel'},
    { key: 'Résidentiel', text: 'Résidentiel'},
    { key: 'Terrain Agricole', text: 'Terrain Agricole' },
    { key: 'Terrain Construit', text: 'Terrain Construit' },
    { key: 'Terrain Urbain', text: 'Terrain Urbain' },
    { key: 'Terrain Villa', text: 'Terrain Villa' },
    { key: 'Unité industrielle', text: 'Unité industrielle' },
    { key: 'Villa', text: 'Villa' },
  ];
  const onChange_type_de_bien = (event: React.FormEvent<HTMLDivElement>, item: IDropdownOption): void => {
    let pos = form.type_de_bien.indexOf(item.key);
    if(pos === -1 && item.selected){
      form.type_de_bien.push(item.text);
    }
    if(pos > -1 && !item.selected){
      let removedItem = form.type_de_bien.splice(pos, 1);
    }
  };
  const _onChange_type_rapport = (ev: React.FormEvent<HTMLInputElement>, isChecked: boolean):void => {
    let pos = form.type_rapport.indexOf(ev.currentTarget.title);
    if(pos === -1 && isChecked && ev.currentTarget.title !== "Tous" && form.type_rapport[0] !== "Tous"){
      form.type_rapport.push(ev.currentTarget.title);
    }
    else if(pos === -1 && isChecked && ev.currentTarget.title !== "Tous" && form.type_rapport[0] === "Tous"){
      setAlertTous(true);
      form.type_rapport = [];
    }
    else if(pos === -1 && isChecked && ev.currentTarget.title === "Tous"){
      form.type_rapport = ["Tous"];
    }
    if(pos > -1 && !isChecked){
      form.type_rapport.splice(pos, 1);
    }
  };
  async function _onSubmit(){
    let archive: any[] = [];
    var rest_filterd_list = null;form.annees
    if(form.type_rapport[0] === "Tous")
      for (let i = 2010; i <= (new Date()).getFullYear() ; i++) {
        form.annees.push(i.toString())
      }
    else
    form.annees = form.type_rapport
    await form.annees.forEach( async (element, index) => {
      var queryArchive = function(elm) {
        return elm.Ann_x00e9_e === Number(element);
      };
      await sp.web.lists.getByTitle("Archive").items.getAll().then(async res=>{
        archive = archive.concat(res.filter(queryArchive));
        if (form.annees.length-1 === index){
          rest_filterd_list = await extendDistanceFiltrerRapport(archive, start, DISTANCE_START_FILTRAGE, DISTANCE_END_FILTRAGE);
          props.handleFiltrerRapport(rest_filterd_list, rest_filterd_list.dis);
        }
        setForm({...form,type_de_bien:[], annees:[]});
      })
      .catch(error=>{
        if(error.status === 404 || (error.response.status && error.response.status === 404)){
          setAlertAutorisation(true);
        }
      });
    });
    setSubmitClick(true);
  }
  let rows = [];
  for (let i = 2010; i <= (new Date()).getFullYear() ; i+=2) {
    rows.push(i)
  }
  return (
    <div>
      {alertAutorisation?       
        <Dialog hidden={!alertAutorisation} onDismiss={()=>setAlertAutorisation(false)} dialogContentProps={FiltrageDialogContentProps} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlertAutorisation(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
        :<></>
      }
      {alertTous?       
        <Dialog hidden={!alertTous} onDismiss={()=>setAlertTous(false)} dialogContentProps={dialogContentPropsTous} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlertTous(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
      :<></>}
      {alertDgi?       
        <Dialog hidden={!alertDgi} onDismiss={()=>setAlertDGi(false)} dialogContentProps={dialogContentDGIProps} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlertDGi(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
        :<></>
      }
      <Stack horizontal horizontalAlign="start"> 
        <ActionButton iconProps={{iconName: 'FabricFolderSearch'}} text={props.buttonTitle} onClick={() => setIsOpen(true)}/>
      </Stack>
      <Panel isOpen={isOpen} onDismiss={()=> setIsOpen(false)} headerText="FILTRAGE" closeButtonAriaLabel="Close">
        <Stack tokens={{childrenGap:10}}>
          <Stack tokens={{ childrenGap: 10}}>
            <Label>Année d'archive</Label>
            {rows.map((item, index) => (
              <Stack horizontal horizontalAlign="start" tokens={{childrenGap:65}}>
                <Checkbox  value={1} title={item} label={arch+item} onChange={_onChange_type_rapport}/>
                {item+1 <= (new Date()).getFullYear()?
                  <Checkbox  value={1} title={item+1} label={arch+(item+1)} onChange={_onChange_type_rapport}/>
                  :
                  <Checkbox  value={1} title="Tous" label="Tous" onChange={_onChange_type_rapport}/>
                }
              </Stack>
            ))}
            {(new Date()).getFullYear() % 2 !== 0?
            <Stack horizontal horizontalAlign="start" tokens={{childrenGap:65}}>
                <Checkbox  value={1} title="Tous" label="Tous" onChange={_onChange_type_rapport}/>
              </Stack>
              :<></>
            }
          </Stack>
          <Stack horizontal horizontalAlign="end" tokens={{childrenGap:30}}>
            <PrimaryButton text="Filtrer" onClick={async() => await _onSubmit()}></PrimaryButton>
            <DefaultButton text="Cancel" onClick={() => setIsOpen(false)}></DefaultButton>
          </Stack>
        </Stack>
      </Panel>
    </div>
  );
}

