import { h, component } from 'fpreact';
import { Navbar, NavbarBrand, NavbarNav } from 'mdbreact';
import HeaderItem from './item';
import style from './style';

const Header = component({
	update(model, msg) {
		return model;
	},

	view(model, dispatch) {
		return (
			<Navbar color="light-blue" dark expand="md">
				<NavbarBrand href="/">
					IIOY
				</NavbarBrand>
				<NavbarNav right>
					<HeaderItem path="/lists/now-playing">
						Now playing
					</HeaderItem>
					<HeaderItem path="/lists/upcoming">
						Upcoming
					</HeaderItem>
					<HeaderItem path="/lists/popular">
						Popular
					</HeaderItem>
					<HeaderItem path="/lists/top-rated">
						Top rated
					</HeaderItem>
				</NavbarNav>
			</Navbar>
		);
	},
});

export default Header;
