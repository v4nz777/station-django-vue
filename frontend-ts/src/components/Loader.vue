<template>
  <div
    class="w-12 h-12 mx-auto border-4 border-red-500 rounded-full"
    id="loader"
  ></div>
</template>
<style>
@keyframes loader-rotate {
  0% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
}
#loader {
  border-right-color: transparent;
  animation: loader-rotate 5s linear infinite;
}
</style>
