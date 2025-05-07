<template>
    <div>
        <!-- Main -->
        <div class="loader-circle-80"></div>
    </div>
</template>

<style>

.loader-circle-80 {
	display: inline-block;
	position: relative;
	width: 70px;
	height: 70px;
	border-radius: 100%;
	border: 5px solid transparent;
	border-bottom: 5px solid #4a5fff;
	border-left: 5px solid #4a5fff;
	animation: cssload-spinR 2s linear infinite;
}
.loader-circle-80:before,
.loader-circle-80:after {
	content: '';
	display: block;
	border-radius: 100%;
	position: absolute;
}
.loader-circle-80:before {
	height: 50px;
	width: 50px;
	border: 3px solid transparent;
	border-top: 3px solid #4a5fff;
	border-right: 3px solid #4a5fff;
	animation: cssload-spinL 0.75s linear infinite;
	transform-origin: center center;
	top: 11%;
	left: 11%;
}
.loader-circle-80:after {
	height: 10px;
	width: 10px;
	background: transparent;
	border: 2px solid #4a5fff;
	top: 35.5%;
	left: 35.5%;
}
@keyframes cssload-spinR {
	to {
		transform: rotate(360deg);
	}
}
@keyframes cssload-spinL {
	to {
		transform: rotate(-360deg);
	}
}
</style>
