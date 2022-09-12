import * as React from 'react';
import styles from './DexaMapsAndArchive.module.scss';
import { IDexaMapsAndArchiveProps } from './IDexaMapsAndArchiveProps';
import MapContainer from './MapContainer';

export default class DexaMapsAndArchive extends React.Component<IDexaMapsAndArchiveProps, {}> {
  private old_desc = null;
  constructor(props) {
    super(props);
    this.old_desc=props.description;
    this.state = {old_key: props.description};
  }
  public render(): React.ReactElement<IDexaMapsAndArchiveProps> {
    return (
      <div className={ styles.dexaMapsAndArchive }>
        <div className={ styles.container }>
          <div className={ styles.row }>
            <MapContainer context={this.props.ctx} GoogleKey={this.props.description}/>
          </div>
        </div>
      </div>
    );
  }
}
