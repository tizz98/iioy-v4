import { h } from 'preact';
import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faCircleNotch from '@fortawesome/fontawesome-free-solid/faCircleNotch';

export default (props) => (
    <div className="text-center">
        <FontAwesomeIcon icon={ faCircleNotch } spin size="6x" { ...props } />
    </div>
);
