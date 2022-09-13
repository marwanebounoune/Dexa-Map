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
  let [form, setForm] = React.useState({type_de_bien:[], type_rapport:[]});
  let [alertAutorisation, setAlertAutorisation] = React.useState(false);
  let [alert, setAlert] = React.useState(false);
  let [alertDgi, setAlertDGi] = React.useState(false);
  let lat = getLat(props.latlng);
  let lng = getLng(props.latlng);

  const start = {
    latitude: lat,
    longitude: lng
  };
  const dialogContentProps = {
    type: DialogType.normal,
    title: 'Attention',
    subText: 'Veuillez préciser le type de réference',
  };
  const dialogContentDGIProps = {
    type: DialogType.normal,
    title: 'Oups',
    subText: 'Désolé la zone choisie n\'est pas prise en charge par le système.',
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
    if(pos === -1 && isChecked){
      form.type_rapport.push(ev.currentTarget.title);
    }
    if(pos > -1 && !isChecked){
      form.type_rapport.splice(pos, 1);
    }
  };
  async function _onSubmit(){
    let rapport_classic: any[] = [];
    let grand_rapport: any[] = [];
    let archive: any[] = [];
    var rest_filterd_list = null;
    form.type_rapport.forEach( async (element, index) => {
      var queryArchive = function(elm) {
        return elm.Ann_x00e9_e === Number(element);
      };
      await sp.web.lists.getByTitle("EvalRapports").items.getAll().then(async res=>{
        console.log("element", element)
        console.log("res", res)
        if(element === "2022"){
          archive = archive.concat(res.filter(queryArchive));
        }
        else if(element === "2019" || element === "2018" || element === "2017" || element === "2016" || element === "2015" || element === "2014"){
          archive = archive.concat(res.filter(queryArchive));
        }
        console.log("archive", archive)
        if (form.type_rapport.length-1 === index){
          rest_filterd_list = await extendDistanceFiltrerRapport(archive, start,DISTANCE_START_FILTRAGE, DISTANCE_END_FILTRAGE,form.type_de_bien);
          props.handleFiltrerRapport(rest_filterd_list, rest_filterd_list.dis);
        }
        setForm({...form,type_de_bien:[], type_rapport:[]});
      })
      .catch(error=>{
        if(error.status === 404 || (error.response.status && error.response.status === 404)){
          setAlertAutorisation(true);
        }
      });
    });
    setSubmitClick(true);
  }
  return (
    <div>
      {alert?       
        <Dialog hidden={!alert} onDismiss={()=>setAlert(false)} dialogContentProps={dialogContentProps} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlert(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
        :<></>
      }
      {alertAutorisation?       
        <Dialog hidden={!alertAutorisation} onDismiss={()=>setAlertAutorisation(false)} dialogContentProps={FiltrageDialogContentProps} modalProps={modelProps}>
          <DialogFooter>
            <DefaultButton onClick={()=>setAlertAutorisation(false)} text="Cancel" />
          </DialogFooter>
        </Dialog>
        :<></>
      }
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
          <Dropdown placeholder="Selectionner le type de bien" multiSelect label="TYPE DE BIEN" options={options_type_de_bien} styles={dropdownStyles} defaultSelectedKey={form.type_de_bien} onChange={onChange_type_de_bien}/>
          <Stack tokens={{ childrenGap: 10}}>
            <Label>TYPE DE Rapport</Label>
            <Stack horizontal horizontalAlign="start" tokens={{childrenGap:1}}>
              <Checkbox  value={1} title="2022" label="Archive 2022" onChange={_onChange_type_rapport}/>
            </Stack>
            <Stack horizontal horizontalAlign="start" tokens={{childrenGap:1}}>
              <Checkbox  value={3} title="2019" label="Archive 2019" onChange={_onChange_type_rapport}/>
              <Checkbox  value={3} title="2018" label="Archive 2018" onChange={_onChange_type_rapport}/>
            </Stack>
            <Stack horizontal horizontalAlign="start" tokens={{childrenGap:1}}>
              <Checkbox  value={3} title="2017" label="Archive 2017" onChange={_onChange_type_rapport}/>
              <Checkbox  value={3} title="2016" label="Archive 2016" onChange={_onChange_type_rapport}/>
            </Stack>
            <Stack horizontal horizontalAlign="start" tokens={{childrenGap:1}}>
              <Checkbox  value={3} title="2015" label="Archive 2015" onChange={_onChange_type_rapport}/>
              <Checkbox  value={3} title="2014" label="Archive 2014" onChange={_onChange_type_rapport}/>
            </Stack>
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

