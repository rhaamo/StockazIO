<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link :to="{name: 'home'}">StockazIO</router-link></li>
          <li class="breadcrumb-item active">Add new</li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-md-11 mx-auto">
        <b-form @submit="addPart">
        </b-form>
      </div>
    </div>

  </div>
</template>
