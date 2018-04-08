import { h } from 'preact';

export default ({ src, ratio = "16by9" }) => (
    <div className={ `embed-responsive embed-responsive-${ratio}` }>
        <iframe className="embed-responsive-item" src={ src } allowFullScreen />
    </div>
);
