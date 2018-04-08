import { h } from 'preact';

export default ({ poster_url, title, maxWidth = '300px', style = {}, ...otherProps }) => (
    <img
        src={ poster_url }
        className={ `img-fluid ${otherProps.className || ''}` }
        style={ {
            ...style,
            maxWidth,
        } }
        alt={ title }
        { ...otherProps }
    />
);
