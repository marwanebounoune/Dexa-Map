import "@pnp/sp/folders";
import * as React from 'react';
import { ActionButton, Stack,  } from 'office-ui-fabric-react';
import { sp } from '../../Constants';
import "@pnp/sp/webs";
import "@pnp/sp/lists";
import "@pnp/sp/security";
import "@pnp/sp/security/list";
import "@pnp/sp/site-users/web";
import "@pnp/sp/site-groups/web";
import { Dialog } from '@microsoft/sp-dialog';
import styles from "../DexaMapsAndArchive.module.scss";

export interface ISignalerProps {
  idRef: any;
  buttonTitle: string;
  ctx: any;
  user:any;
  nbrSignals:any;
}
export default function SignalerRef (props:ISignalerProps){
  let [userDejaSign, setUserDejaSign]= React.useState(false);

    async function Signaler(){
      let user = await sp.web.currentUser();
      const A = await sp.web.lists.getByTitle("Pins").items.getById(props.idRef)()
      var signaleurs:number[] = A.QuiasignalerId
      if(A.QuiasignalerId === null)
        signaleurs = [user.Id]
      else
        signaleurs.push(user.Id)
      sp.web.lists.getByTitle("Pins").items.getById(props.idRef).update({
        QuiasignalerId: signaleurs,
        Nombredesignalement: ++A.Nombredesignalement,
      }
      ).then(()=>{
        Dialog.alert(`Vous avez signaler la référence avec succès.`);
      })
    //}
    }
    async function userSiganler(){
      let user = await sp.web.currentUser();
      let userDejaSignaler = false
      if(props.user !== null)
        userDejaSignaler = await props.user.includes(user.Id)
      setUserDejaSign(userDejaSignaler)
    }
    React.useEffect(() => {
      userSiganler()
    },[])
    return (
        <div>
          {props.nbrSignals === 3 || userDejaSign ?
            <div><span className={styles.spanInfo}>Cette référence est signaler {props.nbrSignals} fois</span></div>
            :
            <Stack horizontal horizontalAlign="start"> 
              <ActionButton iconProps={{iconName: 'PeopleAlert'}} text={props.buttonTitle+" ("+props.nbrSignals+")"} onClick={() => Signaler()}/>
            </Stack>
          }
        </div>
      );
    }
    
