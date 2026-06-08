<script lang="ts">
	type Cliente = {
		id_cliente: string;
		nombre: string;
		telefono: string;
		email: string;
	};

	type Veterinario = {
		id_veterinario: string;
		nombre: string;
		especialidad: string;
	};

	type Mascota = {
		id_mascota: number;
		nombre: string;
		especie: string;
		raza: string;
		edad: number;
		peso: number;
		id_cliente: string;
	};

	type Cita = {
		id_cita: number;
		fecha: string;
		hora: string;
		id_mascota: number;
		id_veterinario: string;
		motivo: string;
		estado: string;
	};

	const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5000/';

	let clientes = $state<Cliente[]>([]);
	let veterinarios = $state<Veterinario[]>([]);
	let mascotas = $state<Mascota[]>([]);
	let citas = $state<Cita[]>([]);
	let loading = $state(true);
	let message = $state('');
	let error = $state('');
	let tab = $state<'clientes' | 'veterinarios' | 'mascotas' | 'citas'>('clientes');

	let clienteForm = $state({ id_cliente: '', nombre: '', telefono: '', email: '' });
	let veterinarioForm = $state({ id_veterinario: '', nombre: '', especialidad: '' });
	let mascotaForm = $state({
		nombre: '',
		especie: '',
		raza: '',
		edad: 0,
		peso: 0,
		id_cliente: ''
	});
	let citaForm = $state({
		fecha: '',
		hora: '',
		id_mascota: '',
		id_veterinario: '',
		motivo: ''
	});

	const stats = $derived([
		{ label: 'Clientes', value: clientes.length },
		{ label: 'Veterinarios', value: veterinarios.length },
		{ label: 'Mascotas', value: mascotas.length },
		{ label: 'Citas', value: citas.length }
	]);

	async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
		const response = await fetch(`${API_URL}${path}`, {
			...options,
			headers: {
				'Content-Type': 'application/json',
				...(options.headers ?? {})
			}
		});
		const data = await response.json().catch(() => ({}));
		if (!response.ok) {
			throw new Error(data.error ?? 'No se pudo completar la operacion.');
		}
		return data as T;
	}

	async function loadData() {
		loading = true;
		error = '';
		try {
			[clientes, veterinarios, mascotas, citas] = await Promise.all([
				api<Cliente[]>('/api/clientes'),
				api<Veterinario[]>('/api/veterinarios'),
				api<Mascota[]>('/api/mascotas'),
				api<Cita[]>('/api/citas')
			]);
		} catch (err) {
			error = err instanceof Error ? err.message : 'No se pudo cargar la informacion.';
		} finally {
			loading = false;
		}
	}

	async function submit(path: string, body: Record<string, unknown>, onDone: () => void) {
		message = '';
		error = '';
		try {
			await api(path, { method: 'POST', body: JSON.stringify(body) });
			onDone();
			message = 'Registro guardado correctamente.';
			await loadData();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Revise los datos ingresados.';
		}
	}

	function createCliente() {
		submit('/api/clientes', clienteForm, () => {
			clienteForm = { id_cliente: '', nombre: '', telefono: '', email: '' };
		});
	}

	function createVeterinario() {
		submit('/api/veterinarios', veterinarioForm, () => {
			veterinarioForm = { id_veterinario: '', nombre: '', especialidad: '' };
		});
	}

	function createMascota() {
		submit(
			'/api/mascotas',
			{
				...mascotaForm,
				edad: Number(mascotaForm.edad),
				peso: Number(mascotaForm.peso)
			},
			() => {
				mascotaForm = { nombre: '', especie: '', raza: '', edad: 0, peso: 0, id_cliente: '' };
			}
		);
	}

	function createCita() {
		submit(
			'/api/citas',
			{
				...citaForm,
				id_mascota: Number(citaForm.id_mascota)
			},
			() => {
				citaForm = { fecha: '', hora: '', id_mascota: '', id_veterinario: '', motivo: '' };
			}
		);
	}

	$effect(() => {
		loadData();
	});
</script>

<svelte:head>
	<title>Clinica Veterinaria</title>
</svelte:head>

<main class="shell">
	<section class="topbar">
		<div>
			<p class="eyebrow">Sistema de gestion</p>
			<h1>Clinica Veterinaria</h1>
		</div>
		<button type="button" onclick={loadData}>Actualizar</button>
	</section>

	<section class="stats" aria-label="Resumen">
		{#each stats as stat}
			<div class="stat">
				<span>{stat.label}</span>
				<strong>{stat.value}</strong>
			</div>
		{/each}
	</section>

	{#if message}
		<p class="notice success">{message}</p>
	{/if}
	{#if error}
		<p class="notice error">{error}</p>
	{/if}

	<nav class="tabs" aria-label="Modulos">
		<button class:active={tab === 'clientes'} type="button" onclick={() => (tab = 'clientes')}>
			Clientes
		</button>
		<button
			class:active={tab === 'veterinarios'}
			type="button"
			onclick={() => (tab = 'veterinarios')}
		>
			Veterinarios
		</button>
		<button class:active={tab === 'mascotas'} type="button" onclick={() => (tab = 'mascotas')}>
			Mascotas
		</button>
		<button class:active={tab === 'citas'} type="button" onclick={() => (tab = 'citas')}>
			Citas
		</button>
	</nav>

	{#if loading}
		<p class="empty">Cargando...</p>
	{:else if tab === 'clientes'}
		<section class="workspace">
			<form onsubmit={(event) => (event.preventDefault(), createCliente())}>
				<h2>Nuevo cliente</h2>
				<label>DNI <input required minlength="8" maxlength="12" bind:value={clienteForm.id_cliente} /></label>
				<label>Nombre <input required maxlength="120" bind:value={clienteForm.nombre} /></label>
				<label>Telefono <input required minlength="7" maxlength="15" bind:value={clienteForm.telefono} /></label>
				<label>Email <input required type="email" maxlength="160" bind:value={clienteForm.email} /></label>
				<button type="submit">Guardar cliente</button>
			</form>

			<table>
				<thead><tr><th>DNI</th><th>Nombre</th><th>Telefono</th><th>Email</th></tr></thead>
				<tbody>
					{#each clientes as cliente}
						<tr><td>{cliente.id_cliente}</td><td>{cliente.nombre}</td><td>{cliente.telefono}</td><td>{cliente.email}</td></tr>
					{:else}
						<tr><td colspan="4">Sin clientes registrados.</td></tr>
					{/each}
				</tbody>
			</table>
		</section>
	{:else if tab === 'veterinarios'}
		<section class="workspace">
			<form onsubmit={(event) => (event.preventDefault(), createVeterinario())}>
				<h2>Nuevo veterinario</h2>
				<label>ID <input required maxlength="11" bind:value={veterinarioForm.id_veterinario} /></label>
				<label>Nombre <input required maxlength="120" bind:value={veterinarioForm.nombre} /></label>
				<label>Especialidad <input required maxlength="120" bind:value={veterinarioForm.especialidad} /></label>
				<button type="submit">Guardar veterinario</button>
			</form>

			<table>
				<thead><tr><th>ID</th><th>Nombre</th><th>Especialidad</th></tr></thead>
				<tbody>
					{#each veterinarios as veterinario}
						<tr><td>{veterinario.id_veterinario}</td><td>{veterinario.nombre}</td><td>{veterinario.especialidad}</td></tr>
					{:else}
						<tr><td colspan="3">Sin veterinarios registrados.</td></tr>
					{/each}
				</tbody>
			</table>
		</section>
	{:else if tab === 'mascotas'}
		<section class="workspace">
			<form onsubmit={(event) => (event.preventDefault(), createMascota())}>
				<h2>Nueva mascota</h2>
				<label>Nombre <input required maxlength="80" bind:value={mascotaForm.nombre} /></label>
				<label>Especie <input required maxlength="80" bind:value={mascotaForm.especie} /></label>
				<label>Raza <input required maxlength="80" bind:value={mascotaForm.raza} /></label>
				<label>Edad <input required type="number" min="0" max="150" bind:value={mascotaForm.edad} /></label>
				<label>Peso <input required type="number" min="0.01" max="1000" step="0.01" bind:value={mascotaForm.peso} /></label>
				<label>DNI cliente <input required minlength="8" maxlength="12" bind:value={mascotaForm.id_cliente} /></label>
				<button type="submit">Guardar mascota</button>
			</form>

			<table>
				<thead><tr><th>ID</th><th>Nombre</th><th>Especie</th><th>Cliente</th></tr></thead>
				<tbody>
					{#each mascotas as mascota}
						<tr><td>{mascota.id_mascota}</td><td>{mascota.nombre}</td><td>{mascota.especie}</td><td>{mascota.id_cliente}</td></tr>
					{:else}
						<tr><td colspan="4">Sin mascotas registradas.</td></tr>
					{/each}
				</tbody>
			</table>
		</section>
	{:else}
		<section class="workspace">
			<form onsubmit={(event) => (event.preventDefault(), createCita())}>
				<h2>Nueva cita</h2>
				<label>Fecha <input required type="date" bind:value={citaForm.fecha} /></label>
				<label>Hora <input required type="time" bind:value={citaForm.hora} /></label>
				<label>ID mascota <input required type="number" min="1" bind:value={citaForm.id_mascota} /></label>
				<label>ID veterinario <input required maxlength="11" bind:value={citaForm.id_veterinario} /></label>
				<label>Motivo <input required maxlength="240" bind:value={citaForm.motivo} /></label>
				<button type="submit">Agendar cita</button>
			</form>

			<table>
				<thead><tr><th>ID</th><th>Fecha</th><th>Hora</th><th>Mascota</th><th>Veterinario</th><th>Estado</th></tr></thead>
				<tbody>
					{#each citas as cita}
						<tr><td>{cita.id_cita}</td><td>{cita.fecha}</td><td>{cita.hora}</td><td>{cita.id_mascota}</td><td>{cita.id_veterinario}</td><td>{cita.estado}</td></tr>
					{:else}
						<tr><td colspan="6">Sin citas registradas.</td></tr>
					{/each}
				</tbody>
			</table>
		</section>
	{/if}
</main>
