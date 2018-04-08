import { h } from 'preact';
import { Link } from 'preact-router/match';
import style from './style';

const Bubble = ({ href, text }) => (
    <Link
        href={ href }
        className={ style.bubble }
    >
        { text }
    </Link>
);
export default Bubble;
