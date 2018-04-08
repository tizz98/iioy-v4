import { h, Component } from 'preact';
import Title from '../../components/title';
import style from './style';

export default class Home extends Component {
	render() {
		return (
			<div class={style.home}>
				<Title />
				<h1>Home</h1>
				<p>This is the Home component.</p>
			</div>
		);
	}
}
