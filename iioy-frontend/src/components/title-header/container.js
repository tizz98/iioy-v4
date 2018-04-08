import { h } from 'preact';
import { Container } from 'mdbreact';
import style from './style';

export const COLORS = {
    purple: 'purple_gradient',
    peach: 'peach_gradient',
    blue: 'blue_gradient',
    green: 'green_gradient',
    violet: 'violet_gradient',
};
export default ({ children, color = COLORS.purple, height = "300px", backgroundImage = null }) => (
    <div
        className={ style[color] }
        style={ {
            height,
            backgroundImage: backgroundImage ? `url(${backgroundImage})` : null,
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center center',
        } }
    >
        <Container className="d-flex justify-content-center align-items-center" style={ { height } }>
            { children }
        </Container>
    </div>
);
