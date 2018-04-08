import { h } from 'preact';
import missingPoster from '../../assets/img/missing_poster.png';

export default ({ poster_url, title, maxWidth = '300px', style = {}, ...otherProps }) => (
    <img
        src={ poster_url || missingPoster }
        className={ `img-fluid ${otherProps.className || ''}` }
        style={ {
            ...style,
            maxWidth,
        } }
        alt={ title }
        { ...otherProps }
    />
);
