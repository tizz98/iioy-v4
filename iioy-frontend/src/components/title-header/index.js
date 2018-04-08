import { h } from 'preact';
import { Container } from 'mdbreact';
import style from './style';

export const COLORS = {
    purple: 'purple_gradient',
    peach: 'peach_gradient',
    blue: 'blue_gradient',
    green: 'green_gradient',
};
export default ({ text, color = COLORS.purple, height = '300px' }) => (
    <div className={ style[color] }  style={ { height } }>
        <Container className="d-flex justify-content-center align-items-center" style={ { height } }>
            <h1 className="text-center align-self-center white-text">{ text }</h1>
        </Container>
    </div>
);
