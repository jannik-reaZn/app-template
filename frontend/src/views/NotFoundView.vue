<template>
  <UError
    :error="{
      statusCode: 404,
      statusMessage: 'Seite nicht gefunden',
      message: 'Die angeforderte Seite existiert nicht.',
    }"
    :clear="{ label: 'Zur Startseite', to: '/' }"
  />
</template>
