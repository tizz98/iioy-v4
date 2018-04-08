import { h } from 'preact';
import { Link } from 'preact-router/match';
import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faHeart from '@fortawesome/fontawesome-free-solid/faHeart';
import { Col, Container, Row, Footer } from 'mdbreact';
import style from './style';

export default () => (
    <Footer color="blue" className="font-small pt-4 mt-4">
        <Container className="text-left">
            <Row>
                <Col sm="6">
                    <h5 className="title">Is It Out Yet?</h5>
                    <p>
                        IIOY is actively developed by <a href="http://elijahwilson.me" target="_blank" rel="noreferrer noopener">Elijah Wilson</a>.
                        It started as a simple movie website in 2013 but has since grown in both design
                        and architechture.
                    </p>
                </Col>
                <Col sm="6">
                    <Row>
                        <Col sm="12" md="6">
                            <ul className={ style.unstyled_list }>
                                <li><Link href="/">Home</Link></li>
                                <li><Link href="/about">About</Link></li>
                                <li><Link href="/legal">Legal</Link></li>
                            </ul>
                        </Col>
                        <Col sm="12" md="6">
                            <ul className={ style.unstyled_list }>
                                <li><Link href="/lists/now-playing">Now playing</Link></li>
                                <li><Link href="/lists/upcoming">Upcoming</Link></li>
                                <li><Link href="/lists/popular">Popular</Link></li>
                                <li><Link href="/lists/top-rated">Top rated</Link></li>
                            </ul>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Container>
        <div className="footer-copyright text-center">
            <Container fluid>
                IIOY <FontAwesomeIcon icon={ faHeart } className="red-text" /> { new Date().getFullYear() }
            </Container>
        </div>
    </Footer>
);
