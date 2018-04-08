import { h } from 'preact';
import Helmet from "preact-helmet";

const BASE_TITLE = 'IIOY - Is It Out Yet?';

export default ({ title }) => (
    <Helmet title={ `${title || ''}${title ? ' - ' : ''}${BASE_TITLE}` } />
);
