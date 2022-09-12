import "@pnp/sp/folders";
import * as React from 'react';
import { ActionButton, Async, Stack,  } from 'office-ui-fabric-react';
import { sp } from '../../Constants';
import "@pnp/sp/webs";
import "@pnp/sp/lists";
import "@pnp/sp/security";
import "@pnp/sp/security/list";
import "@pnp/sp/site-users/web";
import "@pnp/sp/site-groups/web";
import { Dialog } from '@microsoft/sp-dialog';


export interface ISuppProps {
    idRef: number;
    buttonTitle: string;
    ctx: any;
}
export default function SuppRef (props:ISuppProps){
    async function Supprimer(){
        let user = await sp.web.currentUser();
        await sp.web.lists.getByTitle("Pins").items.getById(props.idRef).update({
            ActeurId: user.Id,
            is_deleted: "Oui",
        }).then(()=>{
            Dialog.alert(`La référence est Supprimer.`);
        })
    }
    return (
        <div>
            <Stack horizontal horizontalAlign="start"> 
                <ActionButton iconProps={{iconName: 'Delete'}} text={props.buttonTitle} onClick={() => Supprimer()}/>
            </Stack>
        </div>
    );
}
